from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from PIL import Image
import requests
import io
import os

app = FastAPI()

# Ganti dengan API key Hugging Face awak
HF_API_KEY = os.getenv("HF_API_KEY", "hf_xxx")  
MODEL_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def query_hf(image_bytes: bytes):
    response = requests.post(
        MODEL_URL,
        headers=headers,
        data=image_bytes
    )
    return response.json()

@app.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    pair: str = Form("EUR/USD"),
    timeframe: str = Form("H1"),
    current_price: float = Form(3390.0)
):
    # Baca gambar
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # Hantar ke Hugging Face model
    result = query_hf(contents)

    # Dummy mapping: kalau label ada 'up', anggap BUY
    label = result[0]["label"].lower() if isinstance(result, list) else "unknown"
    entry = float(current_price)

    if "up" in label or "bull" in label:
        tp = round(entry + 10, 1)
        sl = round(entry - 3, 1)
        signal = "BUY"
    elif "down" in label or "bear" in label:
        tp = round(entry - 10, 1)
        sl = round(entry + 3, 1)
        signal = "SELL"
    else:
        tp = entry
        sl = entry
        signal = "UNKNOWN"

    return JSONResponse(content={
        "pair": pair,
        "timeframe": timeframe,
        "signal": signal,
        "analysis": {
            "entry_price": entry,
            "take_profit": tp,
            "stop_loss": sl,
            "raw_model_output": result
        }
    })
