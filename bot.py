import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from aiohttp import web

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8000))  # Render provides PORT env

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Products", callback_data="products")],
        [InlineKeyboardButton("Finished / Logout", callback_data="logout")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "products":
        await query.edit_message_text(text="You clicked Products!")
    elif query.data == "logout":
        await query.edit_message_text(text="Logged out!")

# Set up bot with webhook
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

# Webhook route for Telegram updates
async def webhook(request):
    update = Update.de_json(await request.json(), app.bot)
    await app.update_queue.put(update)
    return web.Response(text="OK")

# Run aiohttp server for webhook
def run_webhook():
    web_app = web.Application()
    web_app.router.add_post(f"/{TOKEN}", webhook)
    print("Bot webhook running...")
    web.run_app(web_app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    run_webhook()
