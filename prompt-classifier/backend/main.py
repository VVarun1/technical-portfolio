from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PromptReq(BaseModel):
    text: str

CONVERGENT_KEYWORDS = ["what is", "who is", "when did", "define", "calculate"]
DIVERGENT_KEYWORDS = ["how might", "imagine", "brainstorm", "what if", "explore"]

@app.post("/classify")
async def classify(req: PromptReq):
    text = req.text.lower()
    conv_score = sum(1 for k in CONVERGENT_KEYWORDS if k in text)
    div_score = sum(1 for k in DIVERGENT_KEYWORDS if k in text)
    
    label = "Convergent" if conv_score > div_score else "Divergent" if div_score > conv_score else "Neutral"
    return {"label": label, "convergent_score": conv_score, "divergent_score": div_score}
