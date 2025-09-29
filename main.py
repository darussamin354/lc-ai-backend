from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from PIL import Image
import requests
import io
import os

app = FastAPI()

# Hugging Face API Key (letak dalam Environment Variables di Render)
HF_API_KEY = os.getenv("HF_API_KEY", "")
MODEL_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def query_hf(image_bytes: bytes):
    try:
        response = requests.post(
            MODEL_URL,
            headers=headers,
            files={"file": ("image.png", image_bytes)}  # ✅ guna files, ada nama file
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@app.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    pair: str = Form("EUR/USD"),
    timeframe: str = Form("H1"),
    current_price: float = Form(3390.0)
):
    try:
        # Baca gambar
        contents = await file.read()
        Image.open(io.BytesIO(contents))  # validate image boleh dibuka

        # Hantar ke Hugging Face
        result = query_hf(contents)

        # Kalau Hugging Face balas error
        if isinstance(result, dict) and "error" in result:
            return JSONResponse(content={"error_from_huggingface": result}, status_code=400)

        # Ambil label
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

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
