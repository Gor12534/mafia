from fastapi import FastAPI, Request
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes

app = FastAPI()
BOT_TOKEN = os.getenv("BOT_TOKEN")
application = ApplicationBuilder().token(BOT_TOKEN).build()

@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return {"status": "ok"}
