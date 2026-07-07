from fastapi import FastAPI, WebSocket
from engine import OrderBook
import json
import asyncio

app = FastAPI()
ob = OrderBook()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Send current snapshot every second
            await websocket.send_text(json.dumps(ob.get_snapshot()))
            await asyncio.sleep(1)
    except Exception as e:
        print(f"WS Error: {e}")

@app.post("/order")
async def place_order(side: str, price: float, quantity: int):
    # Market orders can be sent with price 0
    order_id = ob.add_order(side, price, quantity)
    return {"status": "success", "order_id": order_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
