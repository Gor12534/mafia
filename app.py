from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def home():
    return HTMLResponse("""
    <html>
        <head><title>Mafia Mini App</title></head>
        <body style="font-family: sans-serif; text-align: center; margin-top: 100px;">
            <h1>🎭 Mafia Mini App</h1>
            <p>Welcome! This is just a placeholder page.</p>
            <p>Later we will add profile and chat here.</p>
        </body>
    </html>
    """)
