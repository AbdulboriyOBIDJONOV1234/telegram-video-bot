# 🎥 Modern Telegram Video Downloader Bot v2.0

<div align="center">

![Bot Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**Professional Telegram bot for downloading videos from 1000+ platforms with AI-powered features**

[Features](#-features) • [Installation](#-installation) • [Deployment](#-deployment) • [Commands](#-commands) • [Screenshots](#-screenshots)

</div>

---

## ✨ Features

### 🎯 Core Features
- 🌐 **1000+ Platform Support** - YouTube, Instagram, TikTok, Facebook, Twitter, Reddit, Pinterest, Vimeo, and more
- 🎨 **Modern UI** - Beautiful inline keyboard interface with emoji-rich design
- 📊 **Quality Selection** - Choose between 360p, 480p, and 720p quality
- ⚡ **Fast Downloads** - Optimized video downloading with progress tracking
- 📱 **Platform Detection** - Automatic platform identification with custom icons

### 🤖 AI-Powered Features
- 🎬 **Smart Quality Recommendation** - AI analyzes video duration and suggests optimal quality
- 📝 **AI Caption Generation** - Automatically generates engaging captions with hashtags
- 🏷️ **Hashtag Suggestions** - Smart hashtag generation based on video content
- 📊 **Video Analysis** - Duration analysis, video type detection (Shorts, Long videos)
- 💡 **Smart Tips** - AI provides recommendations based on video characteristics

### 👨‍💻 Admin Features
- 📊 **Advanced Statistics** - Track users, downloads, popular platforms
- 📢 **Broadcast Messages** - Send announcements to all users
- 🗑️ **Cache Management** - Clear temporary files automatically
- 📤 **Export Statistics** - Download stats as JSON file
- 🔄 **Reset Statistics** - Reset all statistics with confirmation
- 🔒 **Admin Panel** - Secure admin-only commands and callbacks

### 📈 Statistics & Analytics
- 👥 User count tracking
- 📥 Total downloads counter
- 🏆 Platform popularity rankings
- 📊 Average downloads per user
- ⏰ Bot uptime monitoring

---

## 🚀 Installation

### Prerequisites
- Python 3.11 or higher
- FFmpeg (for video processing)
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)

### Method 1: Local Installation

#### 1. Clone Repository
```bash
git clone https://github.com/AbdulboriyOBIDJONOV1234/telegram-video-bot.git
cd telegram-video-bot
```

#### 2. Create Virtual Environment
```bash
python3 -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Install FFmpeg
```bash
# Ubuntu/Debian/Kali
sudo apt update && sudo apt install ffmpeg -y

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

#### 5. Configure Environment Variables
```bash
cp .env.example .env
nano .env
```

Edit `.env` file:
```env
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_telegram_user_id  # Optional
OPENAI_API_KEY=your_openai_key  # Optional
```

**Get Bot Token:** 
1. Open [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the token to `.env` file

**Get Your User ID:**
1. Open [@userinfobot](https://t.me/userinfobot) on Telegram
2. Send any message
3. Copy your user ID to `.env` file

#### 6. Run Bot
```bash
python bot.py
```

✅ Bot is running! Press Ctrl+C to stop.

---

## 🌐 Deployment

### Option 1: Replit (Recommended for Beginners) ⭐

**Free 24/7 hosting with browser-based IDE**

1. **Sign up** at [replit.com](https://replit.com)
2. **Import from GitHub:**
   - Click "Create Repl"
   - Select "Import from GitHub"
   - URL: `https://github.com/AbdulboriyOBIDJONOV1234/telegram-video-bot`
3. **Add Secrets (Environment Variables):**
   - Click 🔒 "Secrets" in left panel
   - Add `BOT_TOKEN` with your bot token
   - Optionally add `ADMIN_ID` with your user ID
4. **Run the bot:**
   - Click ▶️ "Run" button
   - Bot will start automatically!

**Keep Bot Running 24/7:**
1. Sign up at [uptimerobot.com](https://uptimerobot.com) (free)
2. Add new monitor:
   - Type: HTTP(s)
   - URL: Your Replit URL (e.g., `https://telegram-video-bot-username.replit.app`)
   - Interval: 5 minutes
3. UptimeRobot will ping your bot every 5 minutes to keep it awake!

### Option 2: Railway.app

**Free 500 hours/month**

1. Visit [railway.app](https://railway.app)
2. Login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `telegram-video-bot` repository
5. Add Environment Variables:
   - `BOT_TOKEN`: Your bot token
   - `ADMIN_ID`: Your user ID (optional)
6. Deploy! ✅

### Option 3: Heroku

1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Login:
```bash
heroku login
```
3. Create app:
```bash
heroku create your-bot-name
```
4. Set environment variables:
```bash
heroku config:set BOT_TOKEN=your_token_here
heroku config:set ADMIN_ID=your_user_id
```
5. Deploy:
```bash
git push heroku main
```

### Option 4: VPS (Ubuntu/Debian)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv ffmpeg git -y

# Clone repository
git clone https://github.com/AbdulboriyOBIDJONOV1234/telegram-video-bot.git
cd telegram-video-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
nano .env
# Add your BOT_TOKEN and ADMIN_ID

# Run with systemd (always on)
sudo nano /etc/systemd/system/telegram-bot.service
```

Add to service file:
```ini
[Unit]
Description=Telegram Video Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/telegram-video-bot
Environment="PATH=/path/to/telegram-video-bot/venv/bin"
ExecStart=/path/to/telegram-video-bot/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

---

## 📱 Commands

### User Commands
- `/start` - Start the bot and see welcome message
- `/help` - Get help and usage instructions
- `/stats` - View bot statistics

### Admin Commands (requires ADMIN_ID)
- `/admin` - Open admin panel
- `/broadcast <message>` - Send message to all users

### How to Use
1. Send `/start` to start the bot
2. Send any video URL (YouTube, Instagram, TikTok, etc.)
3. Bot analyzes the video with AI
4. Choose quality (AI recommends optimal quality)
5. Download video!

---

## 🎨 Screenshots

### Bot Interface
```
🎬 Salom, Username!

Men zamonaviy video yuklovchi botman! 🚀

✨ Imkoniyatlar:
🌐 1000+ platformani qo'llab-quvvatlash
📱 Instagram, YouTube, TikTok, Facebook
🎯 Sifatni tanlash (360p, 480p, 720p)
⚡ Tez va xavfsiz
🎨 Zamonaviy interfeys
📊 Statistika va tahlil
```

### AI Analysis Example
```
📺 YouTube Video

🎬 Nomi: Amazing Video Title...
⏱ Davomiyligi: 3:45
⚡ Turi: Qisqa video

🤖 AI Tavsiya: O'rta yoki yuqori sifat
⭐ Tavsiya: MEDIUM sifat

📏 Sifatni tanlang:
```

---

## 🛠️ Technology Stack

- **Python 3.11+** - Core programming language
- **python-telegram-bot 22.7** - Telegram Bot API wrapper
- **yt-dlp 2026.3.17** - Universal video downloader
- **Flask 2.3.0** - Web server for keep-alive
- **FFmpeg** - Video processing
- **JSON** - Statistics storage

---

## 🌟 Supported Platforms

<details>
<summary>Click to see full list of 1000+ supported platforms</summary>

- ✅ YouTube (videos, shorts, live streams)
- ✅ Instagram (reels, posts, stories, IGTV)
- ✅ TikTok (videos, sounds)
- ✅ Facebook (videos, watch)
- ✅ Twitter / X (videos, GIFs)
- ✅ Reddit (v.redd.it videos)
- ✅ Pinterest (video pins)
- ✅ Vimeo (videos, private videos with password)
- ✅ Dailymotion
- ✅ Twitch (VODs, clips)
- ✅ LinkedIn (videos)
- ✅ Snapchat (stories, spotlights)
- ✅ VK (videos)
- ✅ Odnoklassniki
- ✅ SoundCloud (as video)
- ✅ Bandcamp
- ✅ And 1000+ more platforms!

</details>

---

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | ✅ Yes | Telegram Bot Token from @BotFather |
| `ADMIN_ID` | ❌ No | Your Telegram User ID for admin features |
| `OPENAI_API_KEY` | ❌ No | OpenAI API key for advanced AI features |

### Bot Features Configuration

You can customize these in `bot.py`:
```python
# Maximum file size (Telegram limit)
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Default quality
DEFAULT_QUALITY = 'medium'  # low, medium, high

# Statistics file
STATS_FILE = 'stats.json'

# Downloads directory
DOWNLOAD_DIR = 'downloads'
```

---

## 📊 Admin Panel Features

### Statistics Dashboard
- 👥 Total users count
- 📥 Total downloads
- 📈 Average downloads per user
- 🏆 Most popular platforms
- ⏰ Bot uptime

### Management Tools
- 🗑️ **Clear Cache** - Remove temporary video files
- 📤 **Export Stats** - Download statistics as JSON
- 🔄 **Reset Stats** - Clear all statistics (with confirmation)
- 📊 **Full Stats** - View detailed statistics with user IDs
- 📢 **Broadcast** - Send messages to all users

### Security
- Admin-only commands protected by user ID check
- Confirmation dialogs for destructive actions
- Secure callback query validation

---

## ⚠️ Limitations

- **Maximum file size:** 50MB (Telegram Bot API limit)
- **Video format:** MP4 (automatically converted)
- **Copyright:** Some videos may be protected by copyright
- **Private videos:** Cannot download private or age-restricted content
- **Playlists:** Playlists are not supported (single videos only)

---

## 🐛 Troubleshooting

### Bot not responding
```bash
# Check if bot is running
ps aux | grep bot.py

# Check logs
tail -f /path/to/bot/logs/bot.log

# Restart bot
systemctl restart telegram-bot  # If using systemd
```

### FFmpeg not found
```bash
# Install FFmpeg
sudo apt install ffmpeg -y

# Verify installation
ffmpeg -version
```

### Video download fails
- Check if URL is valid
- Try with different quality
- Some videos may be region-restricted
- Age-restricted videos cannot be downloaded

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 🤝 Contributing

Contributions are welcome! 

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💝 Support

If you find this bot useful, please:
- ⭐ Star this repository
- 🐛 Report bugs by opening issues
- 💡 Suggest features via issues
- 📢 Share with friends

---

## 👨‍💻 Author

**Abdulboriy OBIDJANOV**
- GitHub: [@AbdulboriyOBIDJONOV1234](https://github.com/AbdulboriyOBIDJONOV1234)
- Telegram: [@Abdulboriy7700](https://t.me/Abdulboriy7700)

---

## 📝 Changelog

### Version 2.0 (Latest)
- ✅ Complete UI/UX redesign with modern interface
- ✅ AI-powered video analysis and quality recommendations
- ✅ Smart hashtag generation
- ✅ AI caption generation
- ✅ Admin panel with advanced features
- ✅ Broadcast messaging system
- ✅ Statistics export/import
- ✅ Cache management
- ✅ Platform-specific optimizations
- ✅ Inline keyboard navigation
- ✅ Progress tracking
- ✅ Enhanced error handling

### Version 1.0
- ✅ Basic video downloading
- ✅ Multiple platform support
- ✅ Quality selection
- ✅ Simple statistics

---

## 🔮 Future Plans

- [ ] Multi-language support (English, Russian, etc.)
- [ ] Video thumbnail preview
- [ ] Audio-only download option
- [ ] Playlist download support
- [ ] Video trim/edit features
- [ ] Cloud storage integration
- [ ] Advanced OpenAI integration
- [ ] User preferences/favorites
- [ ] Download history
- [ ] Video search functionality

---

## ⚠️ Disclaimer

This bot is created for educational purposes only. Please respect copyright laws and terms of service of video platforms. The developers are not responsible for any misuse of this software.

**Use responsibly and legally!**

---

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Universal video downloader
- [FFmpeg](https://ffmpeg.org/) - Video processing tool

---

<div align="center">

**Made with ❤️ by Abdulboriy OBIDJANOV**

⭐ Star this repo if you find it useful!

[Report Bug](https://github.com/AbdulboriyOBIDJONOV1234/telegram-video-bot/issues) • [Request Feature](https://github.com/AbdulboriyOBIDJONOV1234/telegram-video-bot/issues)

</div>
