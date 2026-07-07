from fastapi import FastAPI, WebSocket
from typing import List
import json

app = FastAPI()
# Simplified Yjs-like server for demonstration
# In a real app, this would use y-websocket
class DocumentStore:
    def __init__(self):
        self.docs = {}
        self.clients = {}

    def update_doc(self, doc_id, update):
        if doc_id not in self.docs: self.docs[doc_id] = b""
        self.docs[doc_id] += update
        return self.docs[doc_id]

store = DocumentStore()

@app.websocket("/ws/{doc_id}")
async def websocket_endpoint(websocket: WebSocket, doc_id: str):
    await websocket.accept()
    if doc_id not in store.clients: store.clients[doc_id] = []
    store.clients[doc_id].append(websocket)
    
    try:
        while True:
            data = await websocket.receive_bytes()
            updated_doc = store.update_doc(doc_id, data)
            for client in store.clients[doc_id]:
                if client != websocket:
                    await client.send_bytes(data)
    except:
        store.clients[doc_id].remove(websocket)
