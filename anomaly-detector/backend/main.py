from fastapi import FastAPI
import numpy as np
app = FastAPI()

@app.get("/detect")
async def detect(data: list):
    # Rolling Z-Score detection
    mean = np.mean(data)
    std = np.std(data)
    anomalies = [i for i, x in enumerate(data) if abs(x - mean) > 3 * std]
    return {"anomalies": anomalies}
