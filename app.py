# app.py
import os
import logging
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_DOMAIN = os.environ.get("WEBHOOK_DOMAIN")

if not TOKEN or not WEBHOOK_DOMAIN:
    raise ValueError("BOT_TOKEN and WEBHOOK_DOMAIN must be set")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
bot_app = ApplicationBuilder().token(TOKEN).build()

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Products", callback_data="products")],
        [InlineKeyboardButton("Finished / Logout", callback_data="logout")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "products":
        await query.edit_message_text("You clicked Products!")
    elif query.data == "logout":
        await query.edit_message_text("Logged out!")

bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CallbackQueryHandler(button_handler))

# Initialize the app before handling updates
@app.on_event("startup")
async def on_startup():
    await bot_app.initialize()
    webhook_url = f"{WEBHOOK_DOMAIN}/webhook/{TOKEN}"
    await bot_app.bot.set_webhook(webhook_url)
    logger.info(f"Webhook set to: {webhook_url}")

@app.post(f"/webhook/{TOKEN}")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.update_queue.put(update)  # queue for processing
    return {"ok": True}

@app.on_event("shutdown")
async def on_shutdown():
    await bot_app.stop()
