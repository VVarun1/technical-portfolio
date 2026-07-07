import collections
import time
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Order:
    order_id: int
    side: str  # 'buy' or 'sell'
    price: float
    quantity: int
    timestamp: float

class OrderBook:
    def __init__(self):
        self.bids: List[Order] = []  # Sorted descending
        self.asks: List[Order] = []  # Sorted ascending
        self.trades = []
        self.order_id_counter = 0

    def add_order(self, side, price, quantity):
        self.order_id_counter += 1
        order = Order(self.order_id_counter, side, price, quantity, time.time())
        
        if side == 'buy':
            self.match_buy(order)
        else:
            self.match_sell(order)
        
        return order.order_id

    def match_buy(self, buy_order):
        while buy_order.quantity > 0 and self.asks and buy_order.price >= self.asks[0].price:
            best_ask = self.asks[0]
            match_qty = min(buy_order.quantity, best_ask.quantity)
            
            self.execute_trade(buy_order, best_ask, match_qty)
            
            buy_order.quantity -= match_qty
            best_ask.quantity -= match_qty
            
            if best_ask.quantity == 0:
                self.asks.pop(0)

        if buy_order.quantity > 0:
            self.bids.append(buy_order)
            self.bids.sort(key=lambda x: (-x.price, x.timestamp))

    def match_sell(self, sell_order):
        while sell_order.quantity > 0 and self.bids and sell_order.price <= self.bids[0].price:
            best_bid = self.bids[0]
            match_qty = min(sell_order.quantity, best_bid.quantity)
            
            self.execute_trade(best_bid, sell_order, match_qty)
            
            sell_order.quantity -= match_qty
            best_bid.quantity -= match_qty
            
            if best_bid.quantity == 0:
                self.bids.pop(0)

        if sell_order.quantity > 0:
            self.asks.append(sell_order)
            self.asks.sort(key=lambda x: (x.price, x.timestamp))

    def execute_trade(self, buy_order, sell_order, qty):
        price = sell_order.price if sell_order.price > 0 else buy_order.price
        trade = {
            "price": price,
            "quantity": qty,
            "timestamp": time.time(),
            "buy_id": buy_order.order_id,
            "sell_id": sell_order.order_id
        }
        self.trades.append(trade)

    def get_snapshot(self):
        return {
            "bids": [{"price": o.price, "qty": o.quantity} for o in self.bids[:10]],
            "asks": [{"price": o.price, "qty": o.quantity} for o in self.asks[:10]],
            "last_trades": self.trades[-10:]
        }
