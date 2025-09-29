from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from PIL import Image
import io

# WAJIB: buat app object
app = FastAPI()

# Endpoint /analyze
@app.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    pair: str = Form("EUR/USD"),
    timeframe: str = Form("H1"),
    current_price: float = Form(3390.0)
):
    # Baca file gambar
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # Ambil brightness (dummy analysis)
    stat = image.convert("L").getextrema()
    brightness = (stat[1] + stat[0]) / 2

    # Buat kiraan entry, TP, SL
    entry = float(current_price)
    if brightness > 127:
        tp = round(entry + 10, 1)   # naik
        sl = round(entry - 3, 1)
    else:
        tp = round(entry - 10, 1)   # turun
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
