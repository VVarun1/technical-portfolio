from fastapi import FastAPI
app = FastAPI()
@app.get('/var')
async def get_var(): return {'ValueAtRisk': -0.02}