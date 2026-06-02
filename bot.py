#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎥 Modern Telegram Video Downloader Bot
Supports 1000+ platforms with AI-powered features
"""

import os
import logging
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode, ChatAction
import yt_dlp
from dotenv import load_dotenv
import time
from threading import Thread
from flask import Flask
import json
import re
from urllib.parse import urlparse
import requests

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID', '')  # Admin user ID for statistics
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')  # Optional: for AI captions

# Create downloads directory
DOWNLOAD_DIR = 'downloads'
STATS_FILE = 'stats.json'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Flask app for keeping Replit alive
app = Flask('')

@app.route('/')
def home():
    return "🎥 Modern Video Bot is running!"

@app.route('/health')
def health():
    return {"status": "healthy", "bot": "running"}

def run_flask():
    app.run(host='0.0.0.0', port=8080)


# Statistics functions
def load_stats():
    """Load statistics from file"""
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {
        'total_users': set(),
        'total_downloads': 0,
        'downloads_by_platform': {},
        'start_date': datetime.now().isoformat()
    }

def save_stats(stats):
    """Save statistics to file"""
    # Convert set to list for JSON serialization
    stats_copy = stats.copy()
    stats_copy['total_users'] = list(stats_copy['total_users'])
    with open(STATS_FILE, 'w') as f:
        json.dump(stats_copy, f, indent=2)

def update_stats(user_id, platform='unknown'):
    """Update download statistics"""
    stats = load_stats()
    if 'total_users' in stats and isinstance(stats['total_users'], list):
        stats['total_users'] = set(stats['total_users'])
    stats['total_users'].add(user_id)
    stats['total_downloads'] = stats.get('total_downloads', 0) + 1
    stats['downloads_by_platform'][platform] = stats['downloads_by_platform'].get(platform, 0) + 1
    save_stats(stats)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enhanced start command with modern UI"""
    user = update.effective_user
    
    welcome_message = f"""
🎬 *Salom, {user.first_name}!*

Men zamonaviy video yuklovchi botman! 🚀

✨ *Imkoniyatlar:*
🌐 1000+ platformani qo'llab-quvvatlash
📱 Instagram, YouTube, TikTok, Facebook
🎯 Sifatni tanlash (360p, 480p, 720p)
⚡ Tez va xavfsiz
🎨 Zamonaviy interfeys
📊 Statistika va tahlil

🎥 *Qanday foydalanish:*
1️⃣ Video havolasini yuboring
2️⃣ Sifatni tanlang
3️⃣ Videoni oling!

💡 *Buyruqlar:*
/help - Yordam
/stats - Statistika

👨‍💻 *Yaratuvchi:* @YourUsername
🆔 *Bot versiyasi:* 2.0 Pro
"""
    
    # Create inline keyboard
    keyboard = [
        [
            InlineKeyboardButton("📖 Yordam", callback_data="help"),
            InlineKeyboardButton("⚙️ Sozlamalar", callback_data="settings")
        ],
        [
            InlineKeyboardButton("📊 Statistika", callback_data="stats"),
            InlineKeyboardButton("ℹ️ Bot haqida", callback_data="about")
        ],
        [
            InlineKeyboardButton("👨‍💻 Yaratuvchi", url="https://t.me/YourUsername")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enhanced help command"""
    help_text = """
📚 *YORDAM VA YO'RIQNOMA*

🎯 *Qo'llab-quvvatlanadigan platformalar:*
✅ YouTube (shorts ham)
✅ Instagram (reels, posts, stories)
✅ TikTok
✅ Facebook
✅ Twitter / X
✅ Reddit
✅ Pinterest
✅ Vimeo
✅ Dailymotion
✅ 1000+ boshqa platformalar

📝 *Foydalanish:*
1. Video havolasini yuboring
2. Sifat tugmasini bosing
3. Videoni yuklab oling!

⚙️ *Sifat tanlov:*
• 🟢 Yuqori sifat (720p) - kichik videolar uchun
• 🟡 O'rta sifat (480p) - tavsiya etiladi
• 🔴 Past sifat (360p) - katta videolar uchun

⚠️ *Cheklovlar:*
• Maksimal fayl hajmi: 50MB (Telegram cheklovi)
• Katta videolar past sifatda yuklanadi
• Ba'zi videolar mualliflik huquqi bilan himoyalangan

💡 *Maslahatlar:*
• Qisqa videolar (5-10 min) yaxshi ishlaydi
• Shorts va reels tez yuklanadi
• Agar xatolik bo'lsa, qayta urinib ko'ring

🆘 *Muammo bo'lsa:*
Boshqa havola bilan urinib ko'ring yoki @YourUsername ga murojaat qiling
"""
    
    keyboard = [
        [InlineKeyboardButton("🏠 Bosh sahifa", callback_data="start")],
        [InlineKeyboardButton("📊 Statistika", callback_data="stats")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.message.edit_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot statistics"""
    stats = load_stats()
    
    total_users = len(stats.get('total_users', []))
    total_downloads = stats.get('total_downloads', 0)
    platforms = stats.get('downloads_by_platform', {})
    
    # Get top 5 platforms
    top_platforms = sorted(platforms.items(), key=lambda x: x[1], reverse=True)[:5]
    platform_text = "\n".join([f"  • {p}: {c} ta" for p, c in top_platforms])
    
    # Calculate average downloads per user
    avg_downloads = total_downloads / total_users if total_users > 0 else 0
    
    stats_text = f"""
📊 *BOT STATISTIKASI*

👥 *Foydalanuvchilar:* {total_users} ta
📥 *Jami yuklab olingan:* {total_downloads} ta video
📈 *O'rtacha:* {avg_downloads:.1f} video/foydalanuvchi

🏆 *Eng mashhur platformalar:*
{platform_text if platform_text else "  Hali ma'lumot yo'q"}

⏰ *Bot ishlash muddati:*
{stats.get('start_date', 'Ma\'lumot yo\'q')[:10]}

🚀 *Bot holati:* Faol ✅
"""
    
    keyboard = [[InlineKeyboardButton("🏠 Bosh sahifa", callback_data="start")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.message.edit_text(
            stats_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            stats_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin panel - only for admin users"""
    user_id = update.effective_user.id
    
    # Check if user is admin
    if ADMIN_ID and str(user_id) != str(ADMIN_ID):
        await update.message.reply_text(
            "⛔️ Bu buyruq faqat admin uchun!",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    stats = load_stats()
    total_users = len(stats.get('total_users', []))
    total_downloads = stats.get('total_downloads', 0)
    platforms = stats.get('downloads_by_platform', {})
    
    # Detailed statistics
    admin_text = f"""
👨‍💻 *ADMIN PANEL*

📊 *Umumiy statistika:*
👥 Foydalanuvchilar: {total_users}
📥 Yuklab olinganlar: {total_downloads}
📈 O'rtacha: {total_downloads/total_users if total_users > 0 else 0:.2f} video/user

🌐 *Platformalar bo'yicha:*
"""
    
    # All platforms with counts
    for platform, count in sorted(platforms.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_downloads * 100) if total_downloads > 0 else 0
        admin_text += f"  • {platform}: {count} ({percentage:.1f}%)\n"
    
    admin_text += f"""
\n⚙️ *Bot sozlamalari:*
• Maksimal fayl: 50MB
• Qo'llab-quvvatlanadigan formatlar: MP4
• AI tahlil: Faol ✅
• Statistika: Faol ✅

💾 *Server ma'lumotlari:*
• Downloads papka: {len(os.listdir(DOWNLOAD_DIR)) if os.path.exists(DOWNLOAD_DIR) else 0} fayl
• Stats fayl: {'✅ Mavjud' if os.path.exists(STATS_FILE) else '❌ Yo\'q'}
"""
    
    keyboard = [
        [
            InlineKeyboardButton("📊 Full Stats", callback_data="admin_full_stats"),
            InlineKeyboardButton("🗑 Clear Cache", callback_data="admin_clear_cache")
        ],
        [
            InlineKeyboardButton("📤 Export Stats", callback_data="admin_export_stats"),
            InlineKeyboardButton("🔄 Reset Stats", callback_data="admin_reset_stats")
        ],
        [InlineKeyboardButton("🏠 Bosh sahifa", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        admin_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Broadcast message to all users - admin only"""
    user_id = update.effective_user.id
    
    if ADMIN_ID and str(user_id) != str(ADMIN_ID):
        await update.message.reply_text("⛔️ Bu buyruq faqat admin uchun!")
        return
    
    if not context.args:
        await update.message.reply_text(
            "📢 *BROADCAST*\n\n"
            "Foydalanish: /broadcast <xabar>\n\n"
            "Misol:\n"
            "/broadcast Yangi funksiya qo'shildi!",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    message = ' '.join(context.args)
    stats = load_stats()
    users = stats.get('total_users', [])
    
    if not users:
        await update.message.reply_text("❌ Foydalanuvchilar topilmadi!")
        return
    
    status_msg = await update.message.reply_text(
        f"📤 Xabar yuborilmoqda...\n0 / {len(users)}"
    )
    
    success = 0
    failed = 0
    
    for i, user_id in enumerate(users):
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"📢 *ADMIN XABARI*\n\n{message}",
                parse_mode=ParseMode.MARKDOWN
            )
            success += 1
        except Exception as e:
            failed += 1
            logger.error(f"Failed to send to {user_id}: {e}")
        
        # Update status every 10 users
        if (i + 1) % 10 == 0:
            await status_msg.edit_text(
                f"📤 Xabar yuborilmoqda...\n{i+1} / {len(users)}"
            )
    
    await status_msg.edit_text(
        f"✅ *Broadcast tugadi!*\n\n"
        f"📤 Yuborildi: {success}\n"
        f"❌ Xatolik: {failed}",
        parse_mode=ParseMode.MARKDOWN
    )


def detect_platform(url: str) -> str:
    """Detect video platform from URL"""
    url_lower = url.lower()
    if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
        return 'YouTube'
    elif 'instagram.com' in url_lower:
        return 'Instagram'
    elif 'tiktok.com' in url_lower:
        return 'TikTok'
    elif 'facebook.com' in url_lower or 'fb.watch' in url_lower:
        return 'Facebook'
    elif 'twitter.com' in url_lower or 'x.com' in url_lower:
        return 'Twitter'
    elif 'reddit.com' in url_lower:
        return 'Reddit'
    elif 'pinterest.com' in url_lower:
        return 'Pinterest'
    elif 'vimeo.com' in url_lower:
        return 'Vimeo'
    else:
        return 'Other'


def generate_hashtags(title: str, platform: str) -> str:
    """Generate smart hashtags based on video title and platform"""
    # Basic keyword extraction
    words = re.findall(r'\w+', title.lower())
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    keywords = [w for w in words if len(w) > 3 and w not in common_words][:5]
    
    # Platform specific hashtags
    platform_tags = {
        'YouTube': ['#youtube', '#video', '#viral'],
        'Instagram': ['#instagram', '#insta', '#reels'],
        'TikTok': ['#tiktok', '#fyp', '#viral'],
        'Facebook': ['#facebook', '#fb', '#video'],
        'Twitter': ['#twitter', '#tweet', '#video']
    }
    
    hashtags = platform_tags.get(platform, ['#video', '#download'])
    hashtags.extend([f'#{kw}' for kw in keywords[:3]])
    
    return ' '.join(hashtags[:6])


def analyze_video_duration(duration: int) -> dict:
    """Analyze video duration and give recommendations"""
    if duration < 60:
        return {
            'type': 'Shorts',
            'emoji': '⚡',
            'recommendation': 'Yuqori sifat tavsiya etiladi',
            'quality': 'high'
        }
    elif duration < 300:  # 5 minutes
        return {
            'type': 'Qisqa video',
            'emoji': '🎬',
            'recommendation': "O'rta yoki yuqori sifat",
            'quality': 'medium'
        }
    elif duration < 900:  # 15 minutes
        return {
            'type': "O'rta uzunlikdagi video",
            'emoji': '📹',
            'recommendation': "O'rta sifat tavsiya etiladi",
            'quality': 'medium'
        }
    else:
        return {
            'type': 'Uzun video',
            'emoji': '🎥',
            'recommendation': 'Past sifat tavsiya etiladi',
            'quality': 'low'
        }


def generate_ai_caption(title: str, platform: str, duration: int) -> str:
    """Generate smart caption with AI insights"""
    duration_min = duration // 60
    duration_sec = duration % 60
    
    # Format duration
    if duration_min > 0:
        duration_text = f"{duration_min}:{duration_sec:02d}"
    else:
        duration_text = f"{duration_sec}s"
    
    # Generate caption
    caption = f"🎬 *{title[:60]}*\n\n"
    caption += f"📱 Platform: {platform}\n"
    caption += f"⏱ Davomiyligi: {duration_text}\n"
    
    # Add analysis
    analysis = analyze_video_duration(duration)
    caption += f"{analysis['emoji']} Turi: {analysis['type']}\n"
    
    # Add hashtags
    hashtags = generate_hashtags(title, platform)
    caption += f"\n{hashtags}\n"
    
    caption += f"\n💡 *Tavsiya:* {analysis['recommendation']}"
    
    return caption


def smart_quality_selector(duration: int, platform: str) -> str:
    """AI-powered quality selection based on video characteristics"""
    analysis = analyze_video_duration(duration)
    
    # Platform-specific adjustments
    if platform in ['TikTok', 'Instagram'] and duration < 120:
        return 'high'  # Shorts deserve high quality
    
    return analysis['quality']


def get_video_info(url: str) -> dict:
    """Get video information without downloading"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return {
                'success': True,
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', 'Unknown'),
                'views': info.get('view_count', 0),
                'thumbnail': info.get('thumbnail', ''),
                'description': info.get('description', '')[:100]
            }
    except Exception as e:
        logger.error(f"Error getting video info: {e}")
        return {'success': False}


def download_video(url: str, user_id: int, quality: str = 'medium') -> dict:
    """Download video with progress tracking"""
    try:
        user_dir = os.path.join(DOWNLOAD_DIR, str(user_id))
        os.makedirs(user_dir, exist_ok=True)
        
        output_template = os.path.join(user_dir, '%(title)s.%(ext)s')
        
        # Format selection based on quality
        format_options = {
            'low': 'bestvideo[height<=360]+bestaudio/best[height<=360]/worst',
            'medium': 'bestvideo[height<=480]+bestaudio/best[height<=480]/best',
            'high': 'bestvideo[height<=720]+bestaudio/best[height<=720]/best'
        }
        
        ydl_opts = {
            'format': format_options.get(quality, format_options['medium']),
            'outtmpl': output_template,
            'quiet': False,
            'no_warnings': False,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'noplaylist': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info(f"Downloading from: {url} with quality: {quality}")
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Handle different extensions
            if not filename.endswith('.mp4'):
                base_name = os.path.splitext(filename)[0]
                new_filename = base_name + '.mp4'
                if os.path.exists(new_filename):
                    filename = new_filename
            
            if not os.path.exists(filename):
                for file in os.listdir(user_dir):
                    if file.endswith('.mp4'):
                        filename = os.path.join(user_dir, file)
                        break
            
            file_size = os.path.getsize(filename) if os.path.exists(filename) else 0
            
            return {
                'success': True,
                'file_path': filename,
                'title': info.get('title', 'Video'),
                'duration': info.get('duration', 0),
                'size': file_size,
                'too_large': file_size > 50 * 1024 * 1024,
                'platform': detect_platform(url)
            }
    
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        logger.error(f"Download error: {error_msg}")
        
        if 'Sign in to confirm' in error_msg or 'age' in error_msg.lower():
            return {'success': False, 'error': '🔞 Video yosh cheklovi bilan himoyalangan'}
        elif 'Private video' in error_msg or 'private' in error_msg.lower():
            return {'success': False, 'error': '🔒 Video shaxsiy (private)'}
        elif 'not available' in error_msg.lower():
            return {'success': False, 'error': '❌ Video mavjud emas yoki o\'chirilgan'}
        else:
            return {'success': False, 'error': f'❌ Xatolik: {error_msg[:100]}'}
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return {'success': False, 'error': f'⚠️ Kutilmagan xatolik: {str(e)[:100]}'}


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video URL with modern UI"""
    url = update.message.text.strip()
    user_id = update.message.from_user.id
    
    # Validate URL
    if not (url.startswith('http://') or url.startswith('https://')):
        await update.message.reply_text(
            "❌ *Noto'g'ri havola!*\n\n"
            "Iltimos, to'liq video havolasini yuboring.\n"
            "Masalan: `https://youtube.com/watch?v=...`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Detect platform
    platform = detect_platform(url)
    platform_emoji = {
        'YouTube': '📺',
        'Instagram': '📸',
        'TikTok': '🎵',
        'Facebook': '👥',
        'Twitter': '🐦',
        'Reddit': '🤖',
        'Other': '🌐'
    }.get(platform, '🌐')
    
    # Send typing action
    await update.message.chat.send_action(ChatAction.TYPING)
    
    # Get video info first
    status_msg = await update.message.reply_text(
        f"{platform_emoji} *{platform} video topildi!*\n"
        f"⏳ Ma'lumot yuklanmoqda...\n"
        f"🤖 AI tahlil qilinmoqda...",
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Get video information
    video_info = get_video_info(url)
    
    if video_info.get('success'):
        title = video_info['title']
        duration = video_info.get('duration', 0)
        
        # AI Analysis
        analysis = analyze_video_duration(duration)
        recommended_quality = smart_quality_selector(duration, platform)
        
        # Format duration
        duration_min = duration // 60
        duration_sec = duration % 60
        duration_text = f"{duration_min}:{duration_sec:02d}" if duration_min > 0 else f"{duration_sec}s"
        
        # Generate AI caption
        ai_text = f"{platform_emoji} *{platform} Video*\n\n"
        ai_text += f"🎬 *Nomi:* {title[:50]}...\n"
        ai_text += f"⏱ *Davomiyligi:* {duration_text}\n"
        ai_text += f"{analysis['emoji']} *Turi:* {analysis['type']}\n\n"
        ai_text += f"🤖 *AI Tavsiya:* {analysis['recommendation']}\n"
        ai_text += f"⭐ *Tavsiya:* {recommended_quality.upper()} sifat\n\n"
        ai_text += f"📏 *Sifatni tanlang:*"
        
        # Generate hashtags for user
        hashtags = generate_hashtags(title, platform)
        context.user_data['hashtags'] = hashtags
        context.user_data['ai_caption'] = generate_ai_caption(title, platform, duration)
    else:
        ai_text = f"{platform_emoji} *{platform} Video*\n\n"
        ai_text += f"🎬 Video tayyor!\n"
        ai_text += f"📏 Sifatni tanlang:"
        recommended_quality = 'medium'
    
    # Show quality selection with AI recommendation highlight
    keyboard = []
    
    # Highlight recommended quality
    if recommended_quality == 'high':
        keyboard.append([
            InlineKeyboardButton("🟢 Yuqori (720p) ⭐ AI tavsiya", callback_data=f"dl_high_{user_id}"),
        ])
        keyboard.append([
            InlineKeyboardButton("🟡 O'rta (480p)", callback_data=f"dl_medium_{user_id}"),
            InlineKeyboardButton("🔴 Past (360p)", callback_data=f"dl_low_{user_id}")
        ])
    elif recommended_quality == 'low':
        keyboard.append([
            InlineKeyboardButton("🟢 Yuqori (720p)", callback_data=f"dl_high_{user_id}"),
            InlineKeyboardButton("🟡 O'rta (480p)", callback_data=f"dl_medium_{user_id}")
        ])
        keyboard.append([
            InlineKeyboardButton("🔴 Past (360p) ⭐ AI tavsiya", callback_data=f"dl_low_{user_id}"),
        ])
    else:  # medium
        keyboard.append([
            InlineKeyboardButton("🟢 Yuqori (720p)", callback_data=f"dl_high_{user_id}"),
        ])
        keyboard.append([
            InlineKeyboardButton("🟡 O'rta (480p) ⭐ AI tavsiya", callback_data=f"dl_medium_{user_id}"),
        ])
        keyboard.append([
            InlineKeyboardButton("🔴 Past (360p)", callback_data=f"dl_low_{user_id}"),
        ])
    
    keyboard.append([
        InlineKeyboardButton("ℹ️ To'liq ma'lumot", callback_data="video_info"),
        InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Store URL in context for callback
    context.user_data['video_url'] = url
    context.user_data['platform'] = platform
    context.user_data['video_info'] = video_info
    
    await status_msg.edit_text(
        ai_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    # Navigation buttons
    if data == "start":
        await start(Update(update.update_id, message=query.message), context)
        return
    elif data == "help":
        await help_command(update, context)
        return
    elif data == "stats":
        await stats_command(update, context)
        return
    elif data == "about":
        about_text = """
ℹ️ *BOT HAQIDA*

🎥 *Modern Video Downloader Bot*
Versiya: 2.0 🚀

✨ *Xususiyatlar:*
• 1000+ platforma qo'llab-quvvatlash
• Zamonaviy interfeys
• Sifat tanlash
• Tez yuklab olish
• Statistika
• 24/7 ishlash

👨‍💻 *Dasturchi:* @YourUsername
🌐 *GitHub:* github.com/AbdulboriyOBIDJONOV1234
📅 *Yaratilgan:* 2024

💝 Botni ulashing va do'stlaringizga tavsiya eting!
"""
        keyboard = [[InlineKeyboardButton("🏠 Bosh sahifa", callback_data="start")]]
        await query.message.edit_text(
            about_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    elif data == "settings":
        settings_text = """
⚙️ *SOZLAMALAR*

🎨 *Interfeys:* Zamonaviy ✅
📊 *Statistika:* Yoqilgan ✅
🔔 *Bildirishnomalar:* Yoqilgan ✅

Keyinchalik qo'shimcha sozlamalar qo'shiladi...
"""
        keyboard = [[InlineKeyboardButton("🏠 Bosh sahifa", callback_data="start")]]
        await query.message.edit_text(
            settings_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    elif data == "cancel":
        await query.message.edit_text("❌ Bekor qilindi. Boshqa video yuboring!")
        return
    elif data == "video_info":
        video_info = context.user_data.get('video_info', {})
        if video_info.get('success'):
            info_text = f"ℹ️ *TO'LIQ MA'LUMOT*\n\n"
            info_text += f"🎬 *Nomi:* {video_info['title'][:100]}\n\n"
            info_text += f"⏱ *Davomiyligi:* {video_info['duration']//60}:{video_info['duration']%60:02d}\n"
            info_text += f"👤 *Muallif:* {video_info.get('uploader', 'Noma\'lum')}\n"
            
            if video_info.get('views', 0) > 0:
                views = video_info['views']
                if views > 1_000_000:
                    views_text = f"{views/1_000_000:.1f}M"
                elif views > 1_000:
                    views_text = f"{views/1_000:.1f}K"
                else:
                    views_text = str(views)
                info_text += f"👁 *Ko'rishlar:* {views_text}\n"
            
            # Add hashtags
            hashtags = context.user_data.get('hashtags', '')
            if hashtags:
                info_text += f"\n🏷 *Hashtaglar:*\n{hashtags}\n"
            
            info_text += f"\n💡 Sifatni tanlash uchun orqaga qayting"
        else:
            info_text = "❌ Video ma'lumotlari topilmadi"
        
        keyboard = [[InlineKeyboardButton("◀️ Orqaga", callback_data="back_to_quality")]]
        await query.message.edit_text(
            info_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    elif data == "back_to_quality":
        # Recreate quality selection message
        url = context.user_data.get('video_url')
        if url:
            # Simulate message update with quality selection
            await query.message.edit_text(
                "🔄 Sifat tanlash sahifasiga qaytilmoqda...",
                parse_mode=ParseMode.MARKDOWN
            )
        return
    
    # Admin panel callbacks
    if data == "admin_clear_cache":
        if ADMIN_ID and str(query.from_user.id) != str(ADMIN_ID):
            await query.answer("⛔️ Admin emas!", show_alert=True)
            return
        
        # Clear downloads directory
        cleared = 0
        if os.path.exists(DOWNLOAD_DIR):
            for user_dir in os.listdir(DOWNLOAD_DIR):
                user_path = os.path.join(DOWNLOAD_DIR, user_dir)
                if os.path.isdir(user_path):
                    for file in os.listdir(user_path):
                        os.remove(os.path.join(user_path, file))
                        cleared += 1
        
        await query.answer(f"✅ {cleared} ta fayl o'chirildi!", show_alert=True)
        await query.message.edit_text(
            f"🗑 *CACHE TOZALANDI*\n\n{cleared} ta fayl o'chirildi",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    elif data == "admin_export_stats":
        if ADMIN_ID and str(query.from_user.id) != str(ADMIN_ID):
            await query.answer("⛔️ Admin emas!", show_alert=True)
            return
        
        stats = load_stats()
        stats_json = json.dumps(stats, indent=2, ensure_ascii=False)
        
        # Send as file
        await query.message.reply_document(
            document=stats_json.encode('utf-8'),
            filename=f"stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            caption="📊 Bot statistikasi"
        )
        await query.answer("✅ Statistika eksport qilindi!")
        return
    
    elif data == "admin_reset_stats":
        if ADMIN_ID and str(query.from_user.id) != str(ADMIN_ID):
            await query.answer("⛔️ Admin emas!", show_alert=True)
            return
        
        # Confirm reset
        keyboard = [
            [
                InlineKeyboardButton("✅ Ha, tiklash", callback_data="admin_confirm_reset"),
                InlineKeyboardButton("❌ Yo'q", callback_data="admin_cancel_reset")
            ]
        ]
        await query.message.edit_text(
            "⚠️ *OGOHANTIRISH*\n\n"
            "Barcha statistikani o'chirmoqchimisiz?\n"
            "Bu amalni qaytarib bo'lmaydi!",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    
    elif data == "admin_confirm_reset":
        if ADMIN_ID and str(query.from_user.id) != str(ADMIN_ID):
            await query.answer("⛔️ Admin emas!", show_alert=True)
            return
        
        # Reset statistics
        new_stats = {
            'total_users': set(),
            'total_downloads': 0,
            'downloads_by_platform': {},
            'start_date': datetime.now().isoformat()
        }
        save_stats(new_stats)
        
        await query.message.edit_text(
            "✅ *STATISTIKA TIKLANDI*\n\n"
            "Barcha ma'lumotlar o'chirildi",
            parse_mode=ParseMode.MARKDOWN
        )
        await query.answer("Statistika tiklandi!")
        return
    
    elif data == "admin_cancel_reset":
        await query.message.edit_text("❌ Bekor qilindi")
        await query.answer("Bekor qilindi")
        return
    
    elif data == "admin_full_stats":
        if ADMIN_ID and str(query.from_user.id) != str(ADMIN_ID):
            await query.answer("⛔️ Admin emas!", show_alert=True)
            return
        
        stats = load_stats()
        users_list = list(stats.get('total_users', []))
        
        full_stats_text = f"""
📊 *TO'LIQ STATISTIKA*

👥 *Foydalanuvchilar:* {len(users_list)}
📥 *Jami yuklab olinganlar:* {stats.get('total_downloads', 0)}

🆔 *Foydalanuvchilar ID:*
{', '.join(map(str, users_list[:20]))}
{'...' if len(users_list) > 20 else ''}

📅 *Bot ishga tushgan:*
{stats.get('start_date', 'N/A')[:19]}

💾 *Ma'lumotlar:*
• Stats fayl: {os.path.getsize(STATS_FILE) if os.path.exists(STATS_FILE) else 0} bytes
• Downloads: {len(os.listdir(DOWNLOAD_DIR)) if os.path.exists(DOWNLOAD_DIR) else 0} fayllar
"""
        
        keyboard = [[InlineKeyboardButton("◀️ Orqaga", callback_data="start")]]
        await query.message.edit_text(
            full_stats_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    
    # Download buttons
    if data.startswith('dl_'):
        parts = data.split('_')
        quality = parts[1]  # high, medium, low
        user_id = int(parts[2])
        
        # Check if user matches
        if query.from_user.id != user_id:
            await query.answer("❌ Bu sizning videongiz emas!", show_alert=True)
            return
        
        url = context.user_data.get('video_url')
        platform = context.user_data.get('platform', 'Unknown')
        
        if not url:
            await query.message.edit_text("❌ Xatolik: Video topilmadi. Qaytadan havola yuboring.")
            return
        
        # Quality emoji
        quality_emoji = {'high': '🟢', 'medium': '🟡', 'low': '🔴'}.get(quality, '🔵')
        quality_text = {'high': 'Yuqori (720p)', 'medium': 'O\'rta (480p)', 'low': 'Past (360p)'}.get(quality, 'O\'rta')
        
        # Update message
        await query.message.edit_text(
            f"⏳ *Yuklanmoqda...*\n\n"
            f"{quality_emoji} Sifat: {quality_text}\n"
            f"📦 Iltimos kuting...",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Send typing action
        await query.message.chat.send_action(ChatAction.UPLOAD_VIDEO)
        
        try:
            # Download video
            result = download_video(url, user_id, quality)
            
            if result['success']:
                file_path = result['file_path']
                file_size = result['size']
                
                # Check if too large
                if result.get('too_large', False):
                    if quality != 'low':
                        await query.message.edit_text(
                            "⚠️ Video katta. Pastroq sifatda yuklanmoqda..."
                        )
                        result = download_video(url, user_id, 'low')
                        
                        if not result['success'] or result['size'] > 50 * 1024 * 1024:
                            await query.message.edit_text(
                                "❌ *Video juda katta!*\n\n"
                                "Telegram cheklovi: 50MB\n"
                                "Qisqaroq video yoki boshqa havola yuboring.",
                                parse_mode=ParseMode.MARKDOWN
                            )
                            if os.path.exists(file_path):
                                os.remove(file_path)
                            return
                        
                        file_path = result['file_path']
                        file_size = result['size']
                
                # Update status
                file_size_mb = file_size / (1024 * 1024)
                await query.message.edit_text(
                    f"📤 *Yuborilmoqda...*\n\n"
                    f"📦 Hajm: {file_size_mb:.1f} MB\n"
                    f"⏰ Biroz kuting...",
                    parse_mode=ParseMode.MARKDOWN
                )
                
                # Send video with AI-generated caption
                with open(file_path, 'rb') as video_file:
                    # Use AI caption if available
                    ai_caption = context.user_data.get('ai_caption')
                    
                    if ai_caption:
                        caption = ai_caption
                        caption += f"\n\n📦 *Hajm:* {file_size_mb:.1f} MB\n"
                        caption += f"🎨 *Sifat:* {quality_text}\n"
                    else:
                        caption = f"✅ *{result['title'][:50]}...*\n\n"
                        caption += f"📦 Hajm: {file_size_mb:.1f} MB\n"
                        caption += f"🎬 Platform: {platform}\n"
                        caption += f"🎨 Sifat: {quality_text}\n"
                    
                    if result.get('too_large'):
                        caption += "\n⚠️ Sifat avtomatik pasaytirildi"
                    
                    caption += f"\n\n🤖 AI tahlil bilan tayyorlandi"
                    
                    await query.message.reply_video(
                        video=video_file,
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN,
                        supports_streaming=True,
                        read_timeout=120,
                        write_timeout=120
                    )
                
                # Delete status message
                await query.message.delete()
                
                # Update statistics
                update_stats(user_id, result.get('platform', 'unknown'))
                
                # Clean up
                if os.path.exists(file_path):
                    os.remove(file_path)
                
                logger.info(f"Successfully sent video to user {user_id}")
            
            else:
                # Error occurred
                await query.message.edit_text(
                    f"❌ *Xatolik!*\n\n{result['error']}\n\n"
                    "💡 Boshqa havola bilan urinib ko'ring.",
                    parse_mode=ParseMode.MARKDOWN
                )
        
        except Exception as e:
            logger.error(f"Error in callback: {e}")
            await query.message.edit_text(
                f"❌ *Xatolik yuz berdi!*\n\n{str(e)[:100]}\n\n"
                "Iltimos qayta urinib ko'ring.",
                parse_mode=ParseMode.MARKDOWN
            )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enhanced error handler"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ *Xatolik yuz berdi!*\n\n"
            "Iltimos qayta urinib ko'ring yoki /help buyrug'ini yuboring.",
            parse_mode=ParseMode.MARKDOWN
        )


def main():
    """Start the bot with modern features"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found!")
        print("❌ BOT_TOKEN topilmadi! .env faylida sozlang.")
        return
    
    # Start Flask server
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    logger.info("🌐 Flask server started on port 8080")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("🚀 Modern Video Bot started successfully!")
    print("✅ Bot ishga tushdi! Press Ctrl+C to stop.")
    print("🎨 Zamonaviy interfeys va AI funksiyalar faol!")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
