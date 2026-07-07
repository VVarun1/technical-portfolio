from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/predict")
async def predict_next():
    topics = ["AI agents", "Web3", "Rust Programming", "Remote Work", "SaaS Metrics"]
    formats = ["Thread", "Case Study", "Video Tutorial", "Infographic"]
    return {
        "recommended_topic": random.choice(topics),
        "recommended_format": random.choice(formats),
        "predicted_reach": random.randint(1000, 50000)
    }
