# app.py
import os
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CallbackQueryHandler, CommandHandler

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(TOKEN)
app = FastAPI()

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Products", callback_data="products")],
        [InlineKeyboardButton("Finished / Logout", callback_data="logout")]
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

# Telegram webhook endpoint
@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)
    app_builder = ApplicationBuilder().token(TOKEN).build()
    app_builder.add_handler(CommandHandler("start", start))
    app_builder.add_handler(CallbackQueryHandler(button_handler))
    await app_builder.process_update(update)
    return {"ok": True}
