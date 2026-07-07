from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class UserProfile(BaseModel):
    major: str
    gpa: float
    interests: List[str]

SCHOLARSHIPS = [
    {"id": 1, "name": "STEM Excellence", "req_major": "CS", "min_gpa": 3.5},
    {"id": 2, "name": "Arts Grant", "req_major": "Arts", "min_gpa": 3.0},
    {"id": 3, "name": "Global Leader", "req_major": "Political Science", "min_gpa": 3.2},
]

@app.post("/match")
async def match(profile: UserProfile):
    matches = [s for s in SCHOLARSHIPS if s["req_major"] == profile.major and profile.gpa >= s["min_gpa"]]
    return {"matches": matches}
