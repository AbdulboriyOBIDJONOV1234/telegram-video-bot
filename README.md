# 🎥 Telegram Video Downloader Bot

Telegram orqali har qanday platformadan video yuklab olish uchun bot.

A Telegram bot to download videos from any platform.

## 🌟 Xususiyatlari / Features

- ✅ **1000+ platformani qo'llab-quvvatlaydi** / Supports 1000+ platforms
  - YouTube
  - Instagram
  - TikTok
  - Facebook
  - Twitter (X)
  - Reddit
  - Pinterest
  - Vimeo
  - Dailymotion
  - Va ko'p boshqalar / And many more!

- ⚡ **Tez va oson** / Fast and easy
- 🔒 **Xavfsiz** / Secure
- 📱 **Qulay interfeys** / User-friendly interface

## 📋 Talablar / Requirements

- Python 3.8 yoki yuqori / Python 3.8 or higher
- Telegram Bot Token (@BotFather dan oling / Get from @BotFather)

## 🚀 O'rnatish / Installation

### Variant 1: Render.com da deploy qilish (24/7 ishlaydi) ⭐ TAVSIYA ETILADI

1. **Render.com ga ro'yxatdan o'ting**
   - https://render.com ga kiring
   - GitHub akkaunt bilan ro'yxatdan o'ting

2. **New Web Service yarating**
   - Dashboard → "New" → "Web Service"
   - GitHub repository ni ulang: `AbdulboriyOBIDJONOV1234/telegram-video-bot`

3. **Sozlamalarni kiriting**
   - **Name**: `telegram-video-bot` (yoki istalgan nom)
   - **Region**: `Oregon (US West)` yoki `Frankfurt (EU Central)`
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && apt-get update && apt-get install -y ffmpeg`
   - **Start Command**: `python bot.py`
   - **Instance Type**: `Free`

4. **Environment Variables (BOT_TOKEN)**
   - "Add Environment Variable" tugmasini bosing
   - **Key**: `BOT_TOKEN`
   - **Value**: `sizning_bot_tokeningiz`

5. **Deploy qiling**
   - "Create Web Service" tugmasini bosing
   - 5-10 daqiqa kutib, bot deploy bo'ladi! ✅

---

### Variant 2: Mahalliy kompyuterda ishlatish (Local)

#### 1. Repositoryni klonlash / Clone the repository

```bash
git clone https://github.com/AbdulboriyOBIDJONOV1234/telegram-video-bot.git
cd telegram-video-bot
```

#### 2. Virtual muhitni yaratish (tavsiya etiladi) / Create virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 3. Kutubxonalarni o'rnatish / Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. FFmpeg o'rnatish / Install FFmpeg

```bash
# Ubuntu/Debian/Kali Linux
sudo apt update && sudo apt install ffmpeg -y

# macOS
brew install ffmpeg

# Windows
# https://ffmpeg.org/download.html dan yuklab oling
```

#### 5. Bot tokenni sozlash / Configure bot token

`.env.example` faylidan `.env` fayl yarating va bot tokeningizni kiriting:

Copy `.env.example` to `.env` and add your bot token:

```bash
cp .env.example .env
```

`.env` faylini tahrirlang / Edit `.env` file:

```
BOT_TOKEN=your_bot_token_here
```

**Bot token olish / Get bot token:**
1. Telegram'da @BotFather ni oching / Open @BotFather on Telegram
2. `/newbot` buyrug'ini yuboring / Send `/newbot` command
3. Bot uchun nom va username tanlang / Choose name and username
4. Token ni `.env` fayliga qo'ying / Add token to `.env` file

#### 6. Botni ishga tushirish / Start the bot

```bash
python bot.py
```

Botingiz ishga tushdi! ✅ / Your bot is running! ✅

## 💡 Foydalanish / Usage

1. Telegram'da botingizni oching / Open your bot on Telegram
2. `/start` buyrug'ini yuboring / Send `/start` command
3. Video havolasini yuboring / Send a video URL
4. Bot videoni yuklab beradi / Bot will download and send the video

**Misol / Example:**
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## 📝 Buyruqlar / Commands

- `/start` - Botni ishga tushirish / Start the bot
- `/help` - Yordam / Help

## ⚠️ Muhim / Important

- Maksimal fayl hajmi: 50MB (Telegram cheklovi) / Maximum file size: 50MB (Telegram limit)
- Ba'zi videolar mualliflik huquqi bilan himoyalangan bo'lishi mumkin / Some videos may be copyright protected
- Bot faqat shaxsiy foydalanish uchun / Bot is for personal use only

## 🛠️ Texnologiyalar / Technologies

- **python-telegram-bot** - Telegram Bot API
- **yt-dlp** - Video yuklab olish / Video downloader
- **python-dotenv** - Environment variables

## 📜 Litsenziya / License

Bu loyiha MIT litsenziyasi ostida tarqatiladi.

This project is licensed under the MIT License.

## 🤝 Hissa qo'shish / Contributing

Pull requestlar xush kelibsiz! / Pull requests are welcome!

## 📧 Murojaat / Contact

Savollar bo'lsa issue oching yoki pull request yuboring.

For questions, open an issue or submit a pull request.

---

**Eslatma:** Bu bot faqat ta'lim maqsadida yaratilgan. Mualliflik huquqlarini hurmat qiling.

**Note:** This bot is created for educational purposes only. Please respect copyright laws.
