import os
import django
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async
from telegram.error import TelegramError

# Setup Django ORM
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telebot.settings")
django.setup()

from core.models import VideoID

ADMIN_ID = 1755295379
BOT_TOKEN = "8059480461:AAG6b7tPjd_m7KAnlSN2bpkfIr6Dj7jzjrE"


@sync_to_async
def get_video_ids():
    return list(VideoID.objects.values_list("file_id", flat=True))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video_ids = await get_video_ids()
    if not video_ids:
        await update.message.reply_text("No videos found.")
    else:
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
            await update.message.reply_text("No video found in the message.")
    else:
        await update.message.reply_text("❌ You are not allowed to send videos.")


async def delete_webhook(application):
    try:
        # Delete webhook to avoid conflict with polling
        await application.bot.delete_webhook()
        print("Webhook deleted successfully.")
    except TelegramError as e:
        print(f"Failed to delete webhook: {e}")


async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Delete webhook before starting polling to avoid conflict
    await delete_webhook(app)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VIDEO, video_info))

    print("Bot started polling...")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
