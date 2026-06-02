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


def download_video(url: str, user_id: int) -> dict:
    """Download video using yt-dlp and return file info."""
    try:
        # Create user-specific download directory
        user_dir = os.path.join(DOWNLOAD_DIR, str(user_id))
        os.makedirs(user_dir, exist_ok=True)
        
        # Output template
        output_template = os.path.join(user_dir, '%(title)s.%(ext)s')
        
        # yt-dlp options
        ydl_opts = {
            'format': 'best[ext=mp4]/best',  # Prefer MP4 format
            'outtmpl': output_template,
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'noplaylist': True,  # Don't download playlists
            'max_filesize': 50 * 1024 * 1024,  # 50MB max (Telegram limit)
        }
        
        # Download video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            # Get the downloaded file path
            filename = ydl.prepare_filename(info)
            
            return {
                'success': True,
                'file_path': filename,
                'title': info.get('title', 'Video'),
                'duration': info.get('duration', 0),
                'size': os.path.getsize(filename) if os.path.exists(filename) else 0
            }
    
    except yt_dlp.utils.DownloadError as e:
        logger.error(f"Download error: {e}")
        return {
            'success': False,
            'error': 'Video yuklab bo\'lmadi. Havola noto\'g\'ri yoki video mavjud emas.'
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {
            'success': False,
            'error': f'Xatolik yuz berdi: {str(e)}'
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
        # Download video
        result = download_video(url, user_id)
        
        if result['success']:
            file_path = result['file_path']
            
            # Check file size
            file_size = result['size']
            if file_size > 50 * 1024 * 1024:  # 50MB
                await status_message.edit_text(
                    "❌ Video juda katta (50MB dan ko'p).\n"
                    "Telegram cheklovi tufayli yuborib bo'lmaydi."
                )
                # Clean up
                if os.path.exists(file_path):
                    os.remove(file_path)
                return
            
            # Update status
            await status_message.edit_text(
                "📤 Video yuklanmoqda...",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Send video to user
            with open(file_path, 'rb') as video_file:
                await update.message.reply_video(
                    video=video_file,
                    caption=f"✅ *{result['title']}*",
                    parse_mode=ParseMode.MARKDOWN,
                    supports_streaming=True,
                    read_timeout=60,
                    write_timeout=60
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
