# MODA — Telegram kiyim do‘koni + Mini App

O‘quv/demo loyiha: Python + FastAPI + aiogram 3. Telegram bot va Telegram ichida ochiladigan responsiv Mini App bitta Render Web Service’da ishlaydi.

## Nimalar bor?

- O‘zbekcha va ruscha interfeys; foydalanuvchi tilni Mini App ichida o‘zgartirishi mumkin.
- Mahsulotlar katalogi, rasmlar, narx, eski narx/chegirma, yangi mahsulot yorlig‘i, tavsif, o‘lcham va ranglar.
- Kategoriya filtri, qidiruv, narx bo‘yicha saralash.
- Mahsulot tafsilotlari oynasi, sevimlilar, savatchaga tez qo‘shish va miqdorni o‘zgartirish.
- Ism, telefon va manzil bilan to‘lovsiz buyurtma so‘rovi.
- Telegram `initData` imzosini serverda tekshirish; narxlar ham server katalogidan qayta hisoblanadi.
- Buyurtmani SQLite’ga yozish va `ADMIN_CHAT_ID` sozlangan bo‘lsa admin’ga Telegram xabar yuborish.
- Render webhook, `/health` health check va Telegram bot menyusidagi Mini App tugmasi.

> Bu tayyor tijoriy platforma emas, o‘quv uchun starter loyiha. Ombor sinxronlash, promo-kod, yetkazib beruvchi integratsiyasi, qaytarishlar, admin panel, analitika va ishlab chiqarish darajasidagi ma’lumotlar bazasi kiritilmagan. To‘lovlar ataylab yo‘q.

## Papkalar

```text
moda_shop_bot/
├── app.py                 # FastAPI, Telegram bot/webhook, buyurtmalar API
├── products.json          # Demo mahsulotlar; shu faylni tahrirlab katalogni yangilang
├── requirements.txt
├── render.yaml            # Render Blueprint sozlamasi
├── .env.example
├── GUIDE_RENDER_UZ.md     # O‘zbek tilida Render qo‘llanmasi
└── static/
    ├── index.html
    ├── styles.css
    └── app.js
```

## Eng tez Render deploy

1. `moda_shop_bot` papkasidagi fayllarni o‘zingizning GitHub repository’ingizga yuklang.
2. Telegram’da [@BotFather](https://t.me/BotFather) orqali bot yarating va tokenni oling.
3. [Render](https://render.com/) → **New +** → **Blueprint** orqali GitHub repository’ni tanlang. Render `render.yaml` faylini o‘qiydi.
4. `TELEGRAM_BOT_TOKEN` qiymatiga BotFather tokenini kiriting. `WEBHOOK_SECRET` Render tomonidan yaratiladi. Birinchi deploy’dan keyin botga `/myid` yuborib chiqqan raqamni `ADMIN_CHAT_ID` qiymatiga kiriting va redeploy qiling.
5. Deploy tugagach, `https://SIZNING-SERVISINGIZ.onrender.com/health` manzili `{"status":"ok"}` qaytarishi kerak.
6. Botga `/start` yuboring. Katalog tugmasi yoki bot menyusidagi **MODA** orqali Mini App ochiladi.

Batafsil yo‘riqnoma: [`GUIDE_RENDER_UZ.md`](GUIDE_RENDER_UZ.md).

## Lokal ishga tushirish (Windows PowerShell)

Python 3.11 yoki 3.12 tavsiya qilinadi.

```powershell
cd moda_shop_bot
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

`.env` faylidagi `TELEGRAM_BOT_TOKEN` qiymatini haqiqiy token bilan almashtiring. Lokal serverni boshlash:

```powershell
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Brauzerda `http://127.0.0.1:8000` ochiladi. Biroq Telegram Mini App URL’i HTTPS bo‘lishi shart. Telegram ichidan lokal ishlatish uchun HTTPS tunnel (masalan, ngrok) oching va uning HTTPS manzilini `WEBAPP_URL` hamda `PUBLIC_BASE_URL` qilib belgilang, so‘ng serverni qayta ishga tushiring. Telegram webhook’ni faqat ochiq HTTPS manzilga yubora oladi.

## Mahsulotlarni o‘zgartirish

`products.json` ichida mahsulot yozuvini nusxalab, `id` qiymatini noyob qiling. `image` — ochiq HTTPS rasm URL’i; `price` va `oldPrice` — so‘mda butun son; `sizes` — o‘lchamlar ro‘yxati; `colors` — `id`, tarjimalar va `hex` rangidan iborat. Til matnlari `name` va `description` ichida `uz`/`ru` kalitlari bilan saqlanadi.

## Muhim cheklovlar

- Render Free web service 15 daqiqa kiruvchi trafik bo‘lmasa uxlab qoladi va qayta uyg‘onishi taxminan bir daqiqa olishi mumkin. Demo uchun mos, doimiy do‘kon uchun pullik xizmatni ko‘rib chiqing.
- Render Free disk vaqtinchalik: SQLite’dagi buyurtmalar restart, redeploy yoki uxlab uyg‘onish vaqtida yo‘qolishi mumkin. Admin’ga yuborilgan Telegram xabar alohida chatda qoladi, ammo to‘liq buyurtma tarixi uchun PostgreSQL va zaxiralash sozlang.
- Rasmlar demo uchun tashqi Unsplash URL’laridan olinadi. Haqiqiy do‘kon uchun o‘zingizga tegishli mahsulot rasmlarini ishlating.
- Bot tokenini GitHub’ga, `app.py` ichiga yoki ommaviy joyga yozmang. Uni faqat Render Environment Variables’da saqlang.
