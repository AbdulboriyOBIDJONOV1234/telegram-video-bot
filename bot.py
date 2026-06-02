#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Video Downloader Bot
Supports: YouTube, Instagram, TikTok, Facebook, Twitter, and many more platforms
"""

import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
import yt_dlp
from dotenv import load_dotenv
import time
from threading import Thread
from flask import Flask

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

# Create downloads directory if it doesn't exist
DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Flask app for keeping Replit alive
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    welcome_message = """
🎥 *Video Downloader Bot*

Salom! Men sizga turli platformalardan videolarni yuklab beraman.

*Qo'llab-quvvatlanadigan platformalar:*
✅ YouTube
✅ Instagram
✅ TikTok
✅ Facebook
✅ Twitter (X)
✅ Reddit
✅ Pinterest
✅ Va ko'p boshqa platformalar!

*Foydalanish:*
Menga video havolasini yuboring va men uni yuklab beraman.

*Buyruqlar:*
/start - Botni ishga tushirish
/help - Yordam
"""
    await update.message.reply_text(
        welcome_message,
        parse_mode=ParseMode.MARKDOWN
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = """
📖 *Yordam*

*Qanday foydalanish kerak?*
1. Video havolasini menga yuboring
2. Men videoni yuklab olaman
3. Video sizga yuboriladi

*Maslahat:*
- Katta videolar biroz vaqt olishi mumkin
- Ba'zi videolar mualliflik huquqi bilan himoyalangan bo'lishi mumkin

*Qo'llab-quvvatlanadigan platformalar:*
YouTube, Instagram, TikTok, Facebook, Twitter, Reddit, Pinterest, Vimeo, Dailymotion va 1000+ dan ortiq saytlar.

Muammo bo'lsa, yana urinib ko'ring yoki boshqa havola yuboring.
"""
    await update.message.reply_text(
        help_text,
        parse_mode=ParseMode.MARKDOWN
    )


def download_video(url: str, user_id: int, quality: str = 'medium') -> dict:
    """Download video using yt-dlp and return file info."""
    try:
        # Create user-specific download directory
        user_dir = os.path.join(DOWNLOAD_DIR, str(user_id))
        os.makedirs(user_dir, exist_ok=True)
        
        # Output template
        output_template = os.path.join(user_dir, '%(title)s.%(ext)s')
        
        # Format selection based on quality
        if quality == 'low':
            format_string = 'bestvideo[ext=mp4][height<=360]+bestaudio[ext=m4a]/best[ext=mp4][height<=360]/best[height<=360]/worst'
        elif quality == 'medium':
            format_string = 'bestvideo[ext=mp4][height<=480]+bestaudio[ext=m4a]/best[ext=mp4][height<=480]/best[height<=480]/best'
        else:  # high quality but still limited
            format_string = 'bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4][height<=720]/best[height<=720]/best'
        
        # yt-dlp options - Updated for better YouTube support and file size control
        ydl_opts = {
            'format': format_string,
            'outtmpl': output_template,
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'noplaylist': True,
            'cookiefile': None,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'extractor_retries': 3,
            'fragment_retries': 3,
            'skip_unavailable_fragments': True,
            'keepvideo': False,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'merge_output_format': 'mp4',
            'prefer_ffmpeg': True,
            'socket_timeout': 30,
            'http_chunk_size': 10485760,  # 10MB chunks
        }
        
        # Download video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info(f"Downloading from: {url}")
            info = ydl.extract_info(url, download=True)
            
            # Get the downloaded file path
            filename = ydl.prepare_filename(info)
            
            # If file has .webm or other extension, convert to .mp4
            if not filename.endswith('.mp4'):
                base_name = os.path.splitext(filename)[0]
                new_filename = base_name + '.mp4'
                if os.path.exists(new_filename):
                    filename = new_filename
                elif os.path.exists(filename):
                    # File exists but not converted, use as is
                    pass
                else:
                    # Try to find any file in the directory
                    for file in os.listdir(user_dir):
                        if file.startswith(os.path.basename(base_name)):
                            filename = os.path.join(user_dir, file)
                            break
            
            if not os.path.exists(filename):
                raise Exception("Downloaded file not found")
            
            file_size = os.path.getsize(filename)
            
            return {
                'success': True,
                'file_path': filename,
                'title': info.get('title', 'Video'),
                'duration': info.get('duration', 0),
                'size': file_size,
                'too_large': file_size > 50 * 1024 * 1024
            }
    
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        logger.error(f"Download error: {error_msg}")
        
        # More specific error messages
        if 'Sign in to confirm' in error_msg or 'age' in error_msg.lower():
            return {
                'success': False,
                'error': 'Video yosh cheklovi bilan himoyalangan. Yuklab bo\'lmaydi.'
            }
        elif 'Private video' in error_msg or 'private' in error_msg.lower():
            return {
                'success': False,
                'error': 'Bu video shaxsiy. Yuklab bo\'lmaydi.'
            }
        elif 'not available' in error_msg.lower():
            return {
                'success': False,
                'error': 'Video mavjud emas yoki o\'chirilgan.'
            }
        else:
            return {
                'success': False,
                'error': f'Video yuklab bo\'lmadi: {error_msg[:100]}'
            }
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return {
            'success': False,
            'error': f'Xatolik yuz berdi: {str(e)[:100]}'
        }


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages with video URLs."""
    url = update.message.text.strip()
    user_id = update.message.from_user.id
    
    # Check if message contains a URL
    if not (url.startswith('http://') or url.startswith('https://')):
        await update.message.reply_text(
            "❌ Iltimos, to'g'ri video havolasini yuboring.\n\n"
            "Masalan: https://youtube.com/watch?v=..."
        )
        return
    
    # Send processing message
    status_message = await update.message.reply_text(
        "⏳ Video yuklanmoqda, iltimos kuting...",
        parse_mode=ParseMode.MARKDOWN
    )
    
    try:
        # Try to download video with medium quality first
        result = download_video(url, user_id, quality='medium')
        
        if result['success']:
            file_path = result['file_path']
            file_size = result['size']
            
            # If file is too large, try with lower quality
            if result.get('too_large', False):
                await status_message.edit_text(
                    "⚠️ Video katta. Kichik sifatda yuklanmoqda...",
                    parse_mode=ParseMode.MARKDOWN
                )
                
                # Clean up large file
                if os.path.exists(file_path):
                    os.remove(file_path)
                
                # Try downloading with low quality
                result = download_video(url, user_id, quality='low')
                
                if not result['success']:
                    await status_message.edit_text(
                        f"❌ {result['error']}\n\n"
                        "Video juda katta. Telegram cheklovi: 50MB",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    return
                
                file_path = result['file_path']
                file_size = result['size']
                
                # Check again
                if file_size > 50 * 1024 * 1024:
                    await status_message.edit_text(
                        "❌ Video juda katta (50MB dan ko'p).\n"
                        "Kichik sifatda ham Telegram cheklovidan katta.\n\n"
                        "💡 Tavsiya: Qisqaroq videolarni yuboring.",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    # Clean up
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    return
            
            # Update status
            file_size_mb = file_size / (1024 * 1024)
            await status_message.edit_text(
                f"📤 Video yuborilmoqda... ({file_size_mb:.1f} MB)",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Send video to user
            with open(file_path, 'rb') as video_file:
                quality_note = ""
                if result.get('too_large', False):
                    quality_note = "\n\n⚠️ Video katta bo'lgani uchun sifat pasaytirildi"
                
                await update.message.reply_video(
                    video=video_file,
                    caption=f"✅ *{result['title']}*\n📦 Hajm: {file_size_mb:.1f} MB{quality_note}",
                    parse_mode=ParseMode.MARKDOWN,
                    supports_streaming=True,
                    read_timeout=120,
                    write_timeout=120
                )
            
            # Delete status message
            await status_message.delete()
            
            # Clean up downloaded file
            if os.path.exists(file_path):
                os.remove(file_path)
            
            logger.info(f"Successfully sent video to user {user_id}")
        
        else:
            # Error occurred
            await status_message.edit_text(
                f"❌ {result['error']}\n\n"
                "Iltimos, boshqa havola bilan urinib ko'ring yoki /help buyrug'ini yuboring.",
                parse_mode=ParseMode.MARKDOWN
            )
    
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        await status_message.edit_text(
            f"❌ Xatolik yuz berdi: {str(e)}\n\n"
            "Iltimos, qayta urinib ko'ring.",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Clean up if file exists
        try:
            user_dir = os.path.join(DOWNLOAD_DIR, str(user_id))
            if os.path.exists(user_dir):
                for file in os.listdir(user_dir):
                    file_path = os.path.join(user_dir, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
        except:
            pass


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by updates."""
    logger.error(f"Update {update} caused error {context.error}")


def main():
    """Start the bot."""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found in environment variables!")
        print("❌ BOT_TOKEN topilmadi!")
        print("Iltimos .env faylida BOT_TOKEN ni sozlang.")
        return
    
    # Start Flask server in a separate thread (for Replit keep-alive)
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    logger.info("Flask server started on port 8080 (for Replit keep-alive)")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Register error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Bot started successfully! 🚀")
    print("✅ Bot ishga tushdi! Ctrl+C ni bosib to'xtatishingiz mumkin.")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
