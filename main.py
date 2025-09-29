from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io

app = FastAPI()

# ✅ Allow frontend (Vercel) access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://lc-ai-frontend.vercel.app"],  # tukar ikut domain frontend awak
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "LC AI Backend is running"}

@app.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    pair: str = Form("EUR/USD"),
    timeframe: str = Form("H1"),
    current_price: float = Form(3390.0)
):
    # 📂 Baca gambar upload
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # 🔢 Dummy analisis ikut brightness
    stat = image.convert("L").getextrema()
    brightness = (stat[1] + stat[0]) / 2

    entry = float(current_price)
    if brightness > 127:
        tp = round(entry + 10, 1)  # naik 10 pip
        sl = round(entry - 3, 1)   # SL pendek
    else:
        tp = round(entry - 10, 1)  # turun 10 pip
        sl = round(entry + 3, 1)

    result = {
        "pair": pair,
        "timeframe": timeframe,
        "analysis": {
            "entry_price": round(entry, 1),
            "take_profit": tp,
            "stop_loss": sl,
            "confidence": int(brightness) % 100
        }
    }

    return JSONResponse(content=result)
