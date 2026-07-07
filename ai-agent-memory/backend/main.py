from fastapi import FastAPI
app = FastAPI()

@app.post("/agent/task")
async def run_agent(task: str):
    # Agent Loop: Model -> Tool Call -> Execute -> Feedback -> Loop
    return {"status": "Task completed", "steps": ["searched web", "wrote file"]}
