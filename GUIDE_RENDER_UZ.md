# MODA Telegram botini Render’ga joylash — bosqichma-bosqich

Qo‘llanma Windows kompyuterida loyiha fayllari bor deb hisoblaydi. Bot webhook orqali ishlaydi; Mini App esa shu servisdagi HTTPS sayt sifatida ochiladi. To‘lov yo‘q.

## 1. Telegram bot yaratish

1. Telegram’da [@BotFather](https://t.me/BotFather) ni oching.
2. `/newbot` yuboring.
3. Bot nomini kiriting, masalan `MODA Shop`.
4. Bot username’ini kiriting. U `bot` bilan tugashi kerak, masalan `moda_demo_shop_bot`.
5. BotFather bergan tokenni nusxalang. **Tokenni boshqa odamlarga bermang va GitHub’ga yuklamang.**
6. Yangi bot chatini ochib, bir marta `/start` yuboring.

## 2. Kodni GitHub’ga yuklash

1. [GitHub](https://github.com/) da yangi repository yarating, masalan `moda-shop-bot`.
2. ZIP arxivni kompyuteringizda oching.
3. Arxiv ichidagi `moda_shop_bot` papkasining **ichidagi** fayllarni repository’ning asosiy papkasiga yuklang. `app.py`, `products.json`, `requirements.txt`, `render.yaml` va `static/` papkasi repository root’da bo‘lishi kerak.
4. `.env` faylini GitHub’ga hech qachon yuklamang. Loyihada `.env.example` faqat namuna sifatida bor.
5. `Commit changes` qiling.

## 3. Render’da servis yaratish

1. [Render Dashboard](https://dashboard.render.com/) ga kiring va GitHub hisobingizni ulang.
2. **New + → Blueprint** ni bosing.
3. `moda-shop-bot` repository’sini tanlang va Blueprint’ni deploy qiling. Render `render.yaml` dagi `buildCommand`, `startCommand` va `/health` health check sozlamalarini ishlatadi.
4. Render maxfiy qiymat so‘rasa, `TELEGRAM_BOT_TOKEN` uchun BotFather tokenini kiriting.
5. `WEBHOOK_SECRET` `render.yaml` tomonidan avtomatik yaratiladi. Bu qiymatni o‘zgartirmasdan qoldirish mumkin.
6. Birinchi deploy tugashini Render → **Logs** bo‘limidan tekshiring. Build yoki start xatosi chiqsa, shu logdagi birinchi Python xatosini tuzating.

Agar Blueprint ishlatishni xohlamasangiz, Render’da **New + → Web Service** yarating va ushbu parametrlarni kiriting:

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
- **Health Check Path:** `/health`
- **Runtime:** Python

So‘ng Environment bo‘limida `TELEGRAM_BOT_TOKEN` va `WEBHOOK_SECRET` yarating/kiriting.

## 4. Render Environment Variables

Render servis → **Environment** bo‘limida quyidagilarni tekshiring:

| Kalit | Qiymat |
|---|---|
| `TELEGRAM_BOT_TOKEN` | BotFather bergan maxfiy token |
| `WEBHOOK_SECRET` | Tasodifiy maxfiy satr; faqat harflar, raqamlar, `_` va `-` ishlating |
| `ADMIN_CHAT_ID` | Admin Telegram chat ID’si; avvalcha bo‘sh turishi mumkin |

`RENDER_EXTERNAL_URL` Render tomonidan avtomatik beriladi. Uni odatda qo‘lda kiritish shart emas. Kod shu manzilni webhook va Mini App URL’i uchun ishlatadi. Agar maxsus domen yoki alohida Mini App manzilidan foydalansangiz, `WEBAPP_URL` ni to‘liq `https://...` manziliga sozlashingiz mumkin.

## 5. Admin’ga buyurtmalarni yuborishni yoqish

1. Deploy qilingan botni Telegram’da oching va `/myid` buyrug‘ini yuboring.
2. Bot sizga raqam ko‘rinishidagi Telegram ID’ni qaytaradi.
3. Render → servis → **Environment** ga kiring.
4. `ADMIN_CHAT_ID` nomli environment variable yarating va 2-bosqichdagi raqamni qiymat sifatida kiriting.
5. Saqlang va kerak bo‘lsa **Manual Deploy → Deploy latest commit** ni bosing.
6. Admin akkaunt botga oldin `/start` yuborgan bo‘lishi kerak, shunda bot unga buyurtma haqida xabar jo‘nata oladi.

`ADMIN_CHAT_ID` kiritilmagan bo‘lsa, API buyurtmani lokal SQLite fayliga yozishga urinadi va logga qayd qiladi, lekin admin xabarini yubormaydi.

## 6. Ishlayotganini tekshirish

1. Brauzerda Render servisining aniq URL’ini oching, masalan `https://moda-shop-bot-xxxx.onrender.com`.
2. Katalog, rasmlar, qidiruv, kategoriya filtri va RU/UZ almashtirishni tekshiring.
3. `https://SIZNING-URL/health` manzili `{"status":"ok"}` qaytarishi kerak.
4. Telegram’da botga `/start` yuboring.
5. **Do‘konni ochish** tugmasini bosing. Mini App Telegram oynasida ochilishi kerak.
6. Mahsulotni oching, o‘lcham va rangni tanlang, savatchaga qo‘shing va test buyurtmasi yuboring.
7. `ADMIN_CHAT_ID` to‘g‘ri bo‘lsa, admin chatiga buyurtma raqami, mahsulotlar, jami summa va mijoz ma’lumotlari bor xabar keladi.

Buyurtma API’si `Telegram.WebApp.initData` imzosini tekshiradi. Shu sababli buyurtmani oddiy brauzerda ochilgan sahifadan yuborish ishlamaydi — Mini App’ni botning ichidan oching.

## 7. Bot profilidagi Mini App menyusi

Ilova ishga tushganda kod Telegram bot menyusiga `MODA` tugmasini o‘rnatishga harakat qiladi. Bu ishlamasa, `@BotFather` → `/mybots` → botingiz → **Bot Settings → Menu Button** orqali ham sozlashingiz mumkin. URL sifatida Render servisining `https://...onrender.com` manzilini kiriting.

Telegram Mini App uchun ommaviy HTTPS URL kerak; oddiy `http://localhost` havolasi ishlamaydi.

## 8. Mahsulotlarni yangilash

1. GitHub repository’da `products.json` faylini oching.
2. Mahsulot yozuvini nusxalab, noyob `id` bering.
3. `image` maydoniga ochiq HTTPS rasm manzili qo‘ying.
4. `price` qiymatini so‘mda butun son sifatida kiriting. `oldPrice` chegirma bo‘lmasa `null` bo‘lsin.
5. `category` qiymati `women`, `men`, `accessories` yoki `shoes` dan biri bo‘lsin.
6. `name`, `description`, `sizes`, `colors` maydonlarini to‘ldiring. Tarjima maydonlarida `uz` va `ru` kalitlari bo‘lishi kerak.
7. Commit qiling. Render odatda yangi commit’ni avtomatik deploy qiladi.

## 9. Lokal kompyuterda ishlatish (ixtiyoriy)

Python 3.11/3.12 va PowerShell uchun:

```powershell
cd moda_shop_bot
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

`.env` ichiga `TELEGRAM_BOT_TOKEN` ni kiriting, keyin:

```powershell
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Sahifa `http://127.0.0.1:8000` da ochiladi. Ammo Telegram bot webhook va Telegram Mini App uchun internetdan ochiladigan HTTPS URL kerak. Lokal Telegram testi uchun ngrok singari HTTPS tunnel yarating, keyin `WEBAPP_URL` hamda `PUBLIC_BASE_URL` environment qiymatlarini tunnel URL’iga qo‘ying va serverni qayta ishga tushiring.

## 10. Render Free rejasi va ma’lumotlar haqida muhim eslatma

- Render Free web service 15 daqiqa so‘rov bo‘lmasa uxlaydi; qayta ochilganda taxminan bir daqiqa kutish talab qilinishi mumkin. Demo uchun qulay, do‘konni doimiy ishlatish uchun pullik rejani ko‘rib chiqing.
- Free servis fayl tizimi doimiy emas. `shop.db` dagi buyurtmalar restart, redeploy yoki servis uxlab uyg‘onganda yo‘qolishi mumkin. Admin Telegram xabarlari chatda qoladi, lekin bu ma’lumotlar bazasining o‘rnini bosmaydi.
- Haqiqiy do‘kon uchun PostgreSQL, backup, admin autentifikatsiyasi, log/monitoring va maxfiylik talablarini qo‘shing.
- Demo rasmlar tashqi Unsplash URL’laridan yuklanadi. Haqiqiy savdoda mahsulotlarning o‘zingizga tegishli fotosuratlarini ishlating.
