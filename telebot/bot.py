import os
import django
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async

# Setup Django ORM
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telebot.telebot.settings")
django.setup()

from core.models import VideoID

ADMIN_ID = 1755295379

@sync_to_async
def get_video_ids():
    return list(VideoID.objects.values_list("file_id", flat=True))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video_ids = await get_video_ids()
    for file_id in video_ids:
        await update.message.reply_video(file_id)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")

async def video_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        video = update.message.video
        if video:
            await update.message.reply_text(f"file_id: {video.file_id}")
    else:
        await update.message.reply_text("❌ You are not allowed to send videos.")

app = ApplicationBuilder().token("8059480461:AAG6b7tPjd_m7KAnlSN2bpkfIr6Dj7jzjrE").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.VIDEO, video_info))

if __name__ == "__main__":
    app.run_polling()
