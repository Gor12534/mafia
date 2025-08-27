# app.py
import os
import logging
from telegram import Update
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ----------------------
# Config
# ----------------------
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_DOMAIN = os.environ.get("WEBHOOK_DOMAIN")  # e.g., https://mafia-2lu6.onrender.com

if not TOKEN or not WEBHOOK_DOMAIN:
    raise ValueError("BOT_TOKEN and WEBHOOK_DOMAIN must be set in Render environment variables")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ----------------------
# Initialize Bot & FastAPI
# ----------------------
bot_app = ApplicationBuilder().token(TOKEN).build()
app = FastAPI()

# ----------------------
# Handlers
# ----------------------
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

# Register handlers
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CallbackQueryHandler(button_handler))

# ----------------------
# FastAPI Routes
# ----------------------
@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.post(f"/webhook/{TOKEN}")
# async def telegram_webhook(req: Request):
#     try:
#         data = await req.json()
#         logger.info(f"Received update: {data}")
#         update = Update.de_json(data, bot_app.bot)
#         await bot_app.process_update(update)
#         return {"ok": True}
#     except Exception as e:
#         logger.exception("Error handling update")
#         return {"ok": False, "error": str(e)}



# @app.post(f"/webhook/{TOKEN}")
# async def telegram_webhook(req: Request):
#     try:
#         data = await req.json()
#         logger.info(f"Received update: {data}")
#         # CHANGE: use from_dict instead of de_json
#         update = Update.from_dict(data)
#         await bot_app.process_update(update)
#         return {"ok": True}
#     except Exception as e:
#         logger.exception("Error handling update")
#         return {"ok": False, "error": str(e)}

@app.post(f"/webhook/{TOKEN}")
async def telegram_webhook(req: Request):
    try:
        data = await req.json()
        logger.info(f"Received update: {data}")

        # Correct way in v21.11
        update = Update.de_json(data, bot_app.bot)

        await bot_app.process_update(update)
        return {"ok": True}
    except Exception as e:
        logger.exception("Error handling update")
        return {"ok": False, "error": str(e)}

# ----------------------
# Set webhook on startup
# ----------------------
@app.on_event("startup")
async def on_startup():
    webhook_url = f"{WEBHOOK_DOMAIN}/webhook/{TOKEN}"
    await bot_app.bot.set_webhook(webhook_url)
    logger.info(f"Webhook set to: {webhook_url}")
