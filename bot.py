import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g. https://your-app.onrender.com

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Webhook-based Telegram Bot is live!")

# aiohttp webhook handler
async def handle_webhook(request):
    data = await request.json()
    await app.update_queue.put(data)
    return web.Response()

# main app setup
async def main():
    global app
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # Set Telegram webhook URL
    await app.bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH)

    # aiohttp server
    aio_app = web.Application()
    aio_app.router.add_post(WEBHOOK_PATH, handle_webhook)

    return aio_app

# run server
if __name__ == '__main__':
    web.run_app(main(), port=int(os.environ.get("PORT", 10000)))
