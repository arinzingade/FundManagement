
from collections import deque
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['mydatabase']

latest_doc = db.fund.find_one(sort = [('date', -1)])
if latest_doc:
    latest_nav = latest_doc['nav']
else:
    latest_nav = 0

class AveragePrice:
    
    def average_price(self, arr = [("type", "qty", "price")]):
        q = deque()
        
        for transaction in arr:
            type, qty, price = transaction
            
            if type == "BUY":
                q.append((qty, qty, price))
            
            if type == "SELL":
                curr_qty = qty
                while (curr_qty > 0 and q):
                    front_qty, remaining_qty, front_price = q[0]
                    if remaining_qty >= curr_qty:
                        q[0] = (front_qty, remaining_qty - curr_qty, front_price)
                        break
                    
                    else:
                        curr_qty -= remaining_qty
                        q.popleft()
        
        total_qty = 0
        average_price = 0
        tranches = 0
        
        for elem in q:
            print(elem)
        
        for elem in q:
            print(elem)
            total_qty += elem[1]
            average_price += elem[1]*elem[2]
            tranches += (latest_nav - elem[2]) * elem[0]
        
        print("tranches", tranches)
                    
        if total_qty == 0:
            return (0,0,tranches)
        
        average_price /= total_qty

        
        return (average_price, total_qty, tranches)
    
