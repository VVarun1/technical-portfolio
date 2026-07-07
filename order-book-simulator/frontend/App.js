import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { TrendingUp, ShoppingCart, Trash2 } from 'lucide-react';

const API_BASE = "http://localhost:8001";

const App = () => {
  const [snapshot, setSnapshot] = useState({ bids: [], asks: [], last_trades: [] });
  const [order, setOrder] = useState({ side: 'buy', price: 100, quantity: 10 });

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8001/ws");
    ws.onmessage = (event) => {
      setSnapshot(JSON.parse(event.data));
    };
    return () => ws.close();
  }, []);

  const placeOrder = async () => {
    try {
      await axios.post(`${API_BASE}/order`, null, { 
        params: { side: order.side, price: order.price, quantity: order.quantity } 
      });
    } catch (e) {
      console.error("Order failed", e);
    }
  };

  const OrderRow = ({ item, side }) => (
    <div className={`flex justify-between p-2 text-sm border-b ${side === 'buy' ? 'text-green-600 bg-green-50' : 'text-red-600 bg-red-50'}`}>
      <span>${item.price.toFixed(2)}</span>
      <span className="font-mono">{item.qty}</span>
    </div>
  );

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-8 font-mono">
      <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Order Entry */}
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-xl">
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
            <ShoppingCart size={20} /> Place Order
          </h2>
          <div className="space-y-4">
            <div>
              <label className="block text-xs text-slate-400 mb-1">SIDE</label>
              <select 
                className="w-full bg-slate-700 p-2 rounded border border-slate-600"
                value={order.side}
                onChange={e => setOrder({...order, side: e.target.value})}
              >
                <option value="buy">BUY</option>
                <option value="sell">SELL</option>
              </select>
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">PRICE (0 for Market)</label>
              <input 
                type="number" 
                className="w-full bg-slate-700 p-2 rounded border border-slate-600"
                value={order.price}
                onChange={e => setOrder({...order, price: parseFloat(e.target.value)})}
              />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">QUANTITY</label>
              <input 
                type="number" 
                className="w-full bg-slate-700 p-2 rounded border border-slate-600"
                value={order.quantity}
                onChange={e => setOrder({...order, quantity: parseInt(e.target.value)})}
              />
            </div>
            <button 
              onClick={placeOrder}
              className={`w-full p-3 rounded font-bold transition ${order.side === 'buy' ? 'bg-green-600 hover:bg-green-500' : 'bg-red-600 hover:bg-red-500'}`}
            >
              EXECUTE {order.side.toUpperCase()}
            </button>
          </div>
        </div>

        {/* Order Book (DOM) */}
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-xl">
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
            <TrendingUp size={20} /> Order Book
          </h2>
          <div className="space-y-4">
            <div>
              <div className="text-xs text-slate-500 mb-2 uppercase font-bold">Sells (Asks)</div>
              <div className="border rounded overflow-hidden">
                {snapshot.asks.slice().reverse().map((item, i) => <OrderRow key={i} item={item} side="sell" />)}
              </div>
            </div>
            <div className="text-center py-2 border-y border-slate-700 text-lg font-bold text-yellow-400">
              Spread: ${snapshot.asks[0]?.price - snapshot.bids[0]?.price || 0}
            </div>
            <div>
              <div className="text-xs text-slate-500 mb-2 uppercase font-bold">Bids (Buys)</div>
              <div className="border rounded overflow-hidden">
                {snapshot.bids.map((item, i) => <OrderRow key={i} item={item} side="buy" />)}
              </div>
            </div>
          </div>
        </div>

        {/* Trade Tape */}
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-xl">
          <h2 className="text-xl font-bold mb-6">Trade Tape</h2>
          <div className="space-y-2 overflow-y-auto h-[500px]">
            {snapshot.last_trades.map((trade, i) => (
              <div key={i} className="flex justify-between text-xs p-2 bg-slate-700 rounded border-l-4 border-yellow-500">
                <span className="text-slate-300 font-bold">${trade.price.toFixed(2)}</span>
                <span className="text-slate-400">{trade.quantity} units</span>
                <span className="text-slate-500">{new Date(trade.timestamp * 1000).toLocaleTimeString()}</span>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
};

export default App;
