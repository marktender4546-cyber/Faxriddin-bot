from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import sqlite3
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.parse import parse_qsl

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    BotCommand,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    Message,
    Update,
    WebAppInfo,
)
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
PRODUCTS_FILE = BASE_DIR / "products.json"
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", str(BASE_DIR / "shop.db")))

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("moda-shop")

bot: Bot | None = None
dp = Dispatcher()
router = Router()
dp.include_router(router)
user_languages: dict[int, str] = {}

TEXTS = {
    "uz": {
        "welcome": "Assalomu alaykum! 👋\n\n<b>MODA</b> do‘koniga xush kelibsiz. Katalogni Mini App orqali ko‘rishingiz, mahsulotlarni saralashingiz va to‘lovsiz buyurtma so‘rovi yuborishingiz mumkin.",
        "shop": "🛍 Do‘konni ochish",
        "catalog": "👗 Katalog",
        "language": "🌐 Til / Язык",
        "help": "ℹ️ Yordam",
        "contact": "📞 Aloqa",
        "choose_language": "Tilni tanlang / Выберите язык:",
        "language_saved": "Til o‘zgartirildi: O‘zbekcha 🇺🇿",
        "language_saved_ru": "Язык изменён: Русский 🇷🇺",
        "help_text": "<b>Yordam</b>\n1. «Do‘konni ochish» tugmasini bosing.\n2. Mahsulotni tanlang va savatchaga qo‘shing.\n3. Ism, telefon va manzilni kiriting.\n4. Buyurtma so‘rovi admin’ga yuboriladi. To‘lov funksiyasi demo versiyada yo‘q.\n\nMini App to‘g‘ri ishlashi uchun uni Telegram ichida oching.",
        "contact_text": "Savollar bo‘yicha do‘kon adminiga yozing. Admin chat ID olish uchun botda /myid buyrug‘ini yuboring.",
        "open_catalog": "Katalogni Mini App’da oching:",
        "not_configured": "Mini App manzili hali sozlanmagan. Render’da WEBAPP_URL yoki RENDER_EXTERNAL_URL mavjudligini tekshiring.",
        "my_id": "Sizning Telegram chat ID’ingiz: <code>{}</code>\nBu ID’ni Render’dagi ADMIN_CHAT_ID o‘zgaruvchisiga yozing.",
    },
    "ru": {
        "welcome": "Здравствуйте! 👋\n\nДобро пожаловать в магазин <b>MODA</b>. В Mini App можно посмотреть каталог, отфильтровать товары и отправить заявку на заказ без оплаты.",
        "shop": "🛍 Открыть магазин",
        "catalog": "👗 Каталог",
        "language": "🌐 Til / Язык",
        "help": "ℹ️ Помощь",
        "contact": "📞 Контакты",
        "choose_language": "Tilni tanlang / Выберите язык:",
        "language_saved": "Язык изменён: Русский 🇷🇺",
        "language_saved_ru": "Язык изменён: Русский 🇷🇺",
        "help_text": "<b>Помощь</b>\n1. Нажмите «Открыть магазин».\n2. Выберите товар и добавьте его в корзину.\n3. Укажите имя, телефон и адрес.\n4. Заявка отправится администратору. Оплата в демо-версии не предусмотрена.\n\nДля корректной работы открывайте Mini App внутри Telegram.",
        "contact_text": "По вопросам напишите администратору магазина. Чтобы узнать Telegram chat ID, отправьте боту команду /myid.",
        "open_catalog": "Откройте каталог в Mini App:",
        "not_configured": "Адрес Mini App ещё не настроен. Проверьте WEBAPP_URL или RENDER_EXTERNAL_URL в Render.",
        "my_id": "Ваш Telegram chat ID: <code>{}</code>\nУкажите этот ID в переменной ADMIN_CHAT_ID на Render.",
    },
}


def get_webapp_url() -> str | None:
    value = os.getenv("WEBAPP_URL") or os.getenv("RENDER_EXTERNAL_URL")
    return value.rstrip("/") if value else None


def get_public_base_url() -> str | None:
    value = os.getenv("PUBLIC_BASE_URL") or os.getenv("RENDER_EXTERNAL_URL")
    return value.rstrip("/") if value else None


def get_language(user_id: int | None, language_code: str | None = None) -> str:
    if user_id is not None and user_id in user_languages:
        return user_languages[user_id]
    return "ru" if (language_code or "").lower().startswith("ru") else "uz"


def load_products() -> list[dict]:
    with PRODUCTS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def main_keyboard(lang: str) -> InlineKeyboardMarkup:
    url = get_webapp_url()
    rows: list[list[InlineKeyboardButton]] = []
    if url:
        rows.append([InlineKeyboardButton(text=TEXTS[lang]["shop"], web_app=WebAppInfo(url=url))])
    rows.append([
        InlineKeyboardButton(text=TEXTS[lang]["catalog"], callback_data="catalog"),
        InlineKeyboardButton(text=TEXTS[lang]["language"], callback_data="language"),
    ])
    rows.append([
        InlineKeyboardButton(text=TEXTS[lang]["help"], callback_data="help"),
        InlineKeyboardButton(text=TEXTS[lang]["contact"], callback_data="contact"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🇺🇿 O‘zbekcha", callback_data="setlang:uz"),
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="setlang:ru"),
    ]])


def catalog_keyboard(lang: str) -> InlineKeyboardMarkup:
    url = get_webapp_url()
    if not url:
        return main_keyboard(lang)
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=TEXTS[lang]["shop"], web_app=WebAppInfo(url=url))
    ]])


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    user = message.from_user
    lang = get_language(user.id if user else None, user.language_code if user else None)
    if not get_webapp_url():
        await message.answer(TEXTS[lang]["welcome"] + "\n\n" + TEXTS[lang]["not_configured"], reply_markup=main_keyboard(lang))
        return
    await message.answer(TEXTS[lang]["welcome"], reply_markup=main_keyboard(lang))


@router.message(Command("shop"))
async def shop_command(message: Message) -> None:
    user = message.from_user
    lang = get_language(user.id if user else None, user.language_code if user else None)
    if not get_webapp_url():
        await message.answer(TEXTS[lang]["not_configured"])
        return
    await message.answer(TEXTS[lang]["open_catalog"], reply_markup=catalog_keyboard(lang))


@router.message(Command("catalog"))
async def catalog_command(message: Message) -> None:
    user = message.from_user
    lang = get_language(user.id if user else None, user.language_code if user else None)
    products = load_products()[:4]
    await message.answer(TEXTS[lang]["open_catalog"], reply_markup=catalog_keyboard(lang))
    for product in products:
        title = product["name"][lang]
        description = product["description"][lang]
        price = f'{product["price"]:,}'.replace(",", " ")
        caption = f"<b>{escape(title)}</b>\n{escape(description)}\n\n<b>{price} so‘m</b>" if lang == "uz" else f"<b>{escape(title)}</b>\n{escape(description)}\n\n<b>{price} сум</b>"
        try:
            await message.answer_photo(photo=product["image"], caption=caption)
        except Exception as exc:
            logger.warning("Could not send product photo %s: %s", product.get("id"), exc)
            await message.answer(caption)


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    user = message.from_user
    lang = get_language(user.id if user else None, user.language_code if user else None)
    await message.answer(TEXTS[lang]["help_text"], reply_markup=main_keyboard(lang))


@router.message(Command("myid"))
async def myid_command(message: Message) -> None:
    user = message.from_user
    if user:
        lang = get_language(user.id, user.language_code)
        await message.answer(TEXTS[lang]["my_id"].format(user.id))


@router.callback_query(F.data == "language")
async def language_callback(callback: CallbackQuery) -> None:
    lang = get_language(callback.from_user.id, callback.from_user.language_code)
    await callback.message.answer(TEXTS[lang]["choose_language"], reply_markup=language_keyboard())
    await callback.answer()


@router.callback_query(F.data.startswith("setlang:"))
async def set_language_callback(callback: CallbackQuery) -> None:
    lang = callback.data.split(":", maxsplit=1)[1]
    if lang not in TEXTS:
        lang = "uz"
    user_languages[callback.from_user.id] = lang
    saved = TEXTS[lang]["language_saved"] if lang == "uz" else TEXTS[lang]["language_saved_ru"]
    await callback.answer(saved, show_alert=False)
    await callback.message.answer(TEXTS[lang]["welcome"], reply_markup=main_keyboard(lang))


@router.callback_query(F.data == "catalog")
async def catalog_callback(callback: CallbackQuery) -> None:
    lang = get_language(callback.from_user.id, callback.from_user.language_code)
    await callback.message.answer(TEXTS[lang]["open_catalog"], reply_markup=catalog_keyboard(lang))
    await callback.answer()


@router.callback_query(F.data == "help")
async def help_callback(callback: CallbackQuery) -> None:
    lang = get_language(callback.from_user.id, callback.from_user.language_code)
    await callback.message.answer(TEXTS[lang]["help_text"], reply_markup=main_keyboard(lang))
    await callback.answer()


@router.callback_query(F.data == "contact")
async def contact_callback(callback: CallbackQuery) -> None:
    lang = get_language(callback.from_user.id, callback.from_user.language_code)
    await callback.message.answer(TEXTS[lang]["contact_text"])
    await callback.answer()


def validate_telegram_init_data(init_data: str, token: str, max_age_seconds: int = 86400) -> dict:
    """Validate Telegram Mini App initData with Telegram's documented HMAC scheme."""
    values = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = values.pop("hash", None)
    # For bot-token HMAC validation, include every field except `hash` in the data-check string.
    # The `signature` field is excluded only by Telegram's separate third-party Ed25519 validation flow.
    if not received_hash:
        raise ValueError("Missing Telegram initData hash")
    data_check_string = "\n".join(f"{key}={value}" for key, value in sorted(values.items()))
    secret_key = hmac.new(b"WebAppData", token.encode("utf-8"), hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode("utf-8"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(calculated_hash, received_hash):
        raise ValueError("Invalid Telegram initData signature")

    try:
        auth_date = int(values["auth_date"])
    except (KeyError, ValueError) as exc:
        raise ValueError("Invalid auth_date") from exc
    now = int(time.time())
    if auth_date > now + 60 or now - auth_date > max_age_seconds:
        raise ValueError("Telegram initData has expired")

    try:
        user = json.loads(values["user"])
    except (KeyError, json.JSONDecodeError) as exc:
        raise ValueError("Missing or invalid Telegram user") from exc
    if not isinstance(user, dict) or not user.get("id"):
        raise ValueError("Telegram user ID is missing")
    return user


def init_database() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                telegram_id INTEGER NOT NULL,
                customer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                note TEXT NOT NULL,
                items_json TEXT NOT NULL,
                total INTEGER NOT NULL,
                language TEXT NOT NULL
            )"""
        )
        connection.commit()


def insert_order(order: dict) -> int:
    with sqlite3.connect(DATABASE_PATH, timeout=10) as connection:
        cursor = connection.execute(
            """INSERT INTO orders
            (created_at, telegram_id, customer_name, phone, address, note, items_json, total, language)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                datetime.now(timezone.utc).isoformat(), order["telegram_id"], order["customer_name"],
                order["phone"], order["address"], order["note"], json.dumps(order["items"], ensure_ascii=False),
                order["total"], order["language"],
            ),
        )
        connection.commit()
        return int(cursor.lastrowid)


class CartItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    product_id: str = Field(alias="productId", min_length=1, max_length=80)
    quantity: int = Field(ge=1, le=20)
    size: str = Field(min_length=1, max_length=30)
    color: str = Field(min_length=1, max_length=60)


class OrderRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    init_data: str = Field(alias="initData", min_length=1)
    customer_name: str = Field(alias="customerName", min_length=2, max_length=100)
    phone: str = Field(min_length=5, max_length=40)
    address: str = Field(min_length=4, max_length=300)
    note: str = Field(default="", max_length=500)
    language: str = Field(default="uz", min_length=2, max_length=2)
    items: list[CartItem] = Field(min_length=1, max_length=50)


@asynccontextmanager
async def lifespan(_: FastAPI):
    global bot
    init_database()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if token:
        bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        base_url = get_public_base_url()
        if base_url:
            secret = os.getenv("WEBHOOK_SECRET")
            await bot.set_webhook(
                url=f"{base_url}/telegram/webhook",
                secret_token=secret if secret else None,
                allowed_updates=dp.resolve_used_update_types(),
                drop_pending_updates=False,
            )
            app_url = get_webapp_url()
            if app_url:
                try:
                    await bot.set_chat_menu_button(menu_button=MenuButtonWebApp(text="🛍 MODA", web_app=WebAppInfo(url=app_url)))
                except Exception as exc:
                    logger.warning("Could not configure Telegram menu button: %s", exc)
            logger.info("Telegram webhook configured: %s/telegram/webhook", base_url)
        else:
            logger.warning("Bot token exists but PUBLIC_BASE_URL/RENDER_EXTERNAL_URL is missing; webhook was not configured.")
        try:
            await bot.set_my_commands([
                BotCommand(command="start", description="Do‘konni ochish / Открыть магазин"),
                BotCommand(command="shop", description="Katalogni ochish / Каталог"),
                BotCommand(command="catalog", description="Mahsulotlar / Товары"),
                BotCommand(command="help", description="Yordam / Помощь"),
                BotCommand(command="myid", description="Chat ID ni ko‘rish / Узнать chat ID"),
            ])
        except Exception as exc:
            logger.warning("Could not set bot commands: %s", exc)
    else:
        logger.warning("TELEGRAM_BOT_TOKEN is empty. Mini App API works, Telegram bot is disabled.")
    yield
    if bot:
        await bot.session.close()
        bot = None


app = FastAPI(title="MODA Telegram Shop", version="1.0.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
async def homepage() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/api/products")
async def products() -> list[dict]:
    return load_products()


@app.post("/telegram/webhook")
async def telegram_webhook(request: Request) -> JSONResponse:
    if bot is None:
        raise HTTPException(status_code=503, detail="Telegram bot is not configured")
    expected_secret = os.getenv("WEBHOOK_SECRET")
    if expected_secret and not hmac.compare_digest(request.headers.get("X-Telegram-Bot-Api-Secret-Token", ""), expected_secret):
        raise HTTPException(status_code=403, detail="Invalid webhook secret")
    try:
        payload = await request.json()
        update = Update.model_validate(payload, context={"bot": bot})
        await dp.feed_update(bot, update)
    except Exception as exc:
        logger.exception("Failed to process Telegram update: %s", exc)
        raise HTTPException(status_code=400, detail="Could not process Telegram update") from exc
    return JSONResponse({"ok": True})


@app.post("/api/orders")
async def create_order(request_data: OrderRequest) -> dict:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise HTTPException(status_code=503, detail="Telegram bot is not configured")
    try:
        tg_user = validate_telegram_init_data(request_data.init_data, token)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Telegram sessiyasi yaroqsiz. Mini App’ni bot ichidan qayta oching.") from exc

    try:
        product_by_id = {item["id"]: item for item in load_products()}
    except Exception as exc:
        logger.exception("Failed to load product catalog")
        raise HTTPException(status_code=500, detail="Catalog is unavailable") from exc

    normalized_items: list[dict] = []
    total = 0
    for item in request_data.items:
        product = product_by_id.get(item.product_id)
        if not product:
            raise HTTPException(status_code=400, detail=f"Unknown product: {item.product_id}")
        allowed_sizes = product.get("sizes", [])
        allowed_colors = [color["id"] for color in product.get("colors", [])]
        if item.size not in allowed_sizes or item.color not in allowed_colors:
            raise HTTPException(status_code=400, detail=f"Invalid size/color for product: {item.product_id}")
        line_total = int(product["price"]) * item.quantity
        total += line_total
        normalized_items.append({
            "productId": product["id"], "name": product["name"], "price": int(product["price"]),
            "quantity": item.quantity, "size": item.size, "color": item.color, "lineTotal": line_total,
        })

    lang = request_data.language if request_data.language in TEXTS else "uz"
    order = {
        "telegram_id": int(tg_user["id"]), "customer_name": request_data.customer_name.strip(),
        "phone": request_data.phone.strip(), "address": request_data.address.strip(),
        "note": request_data.note.strip(), "items": normalized_items, "total": total, "language": lang,
    }
    try:
        order_id = insert_order(order)
    except Exception as exc:
        logger.exception("Failed to save order")
        raise HTTPException(status_code=500, detail="Buyurtmani saqlashda xatolik yuz berdi.") from exc

    admin_chat_id = os.getenv("ADMIN_CHAT_ID", "").strip()
    if bot and admin_chat_id:
        item_lines = []
        for item in normalized_items:
            name = item["name"].get(lang, item["name"]["uz"])
            color_label = next((c.get(lang, c.get("uz", c["id"])) for c in product_by_id[item["productId"]]["colors"] if c["id"] == item["color"]), item["color"])
            item_lines.append(
                f"• {escape(name)} × {item['quantity']} — {escape(item['size'])}, {escape(color_label)} — "
                f"{item['lineTotal']:,} so‘m".replace(",", " ")
            )
        admin_text = (
            f"🛍 <b>Yangi buyurtma #{order_id}</b>\n\n"
            f"<b>Mijoz:</b> {escape(order['customer_name'])}\n"
            f"<b>Telefon:</b> {escape(order['phone'])}\n"
            f"<b>Manzil:</b> {escape(order['address'])}\n"
            f"<b>Telegram ID:</b> <code>{order['telegram_id']}</code>\n\n"
            f"<b>Tovarlar:</b>\n" + "\n".join(item_lines) +
            f"\n\n<b>Jami:</b> {total:,} so‘m".replace(",", " ") +
            (f"\n<b>Izoh:</b> {escape(order['note'])}" if order["note"] else "")
        )
        try:
            await bot.send_message(chat_id=int(admin_chat_id), text=admin_text)
        except Exception:
            logger.exception("Order #%s was saved, but admin notification failed", order_id)
    else:
        logger.info("Order #%s saved, but ADMIN_CHAT_ID is not configured.", order_id)

    return {"ok": True, "orderId": order_id, "total": total}
