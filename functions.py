
from collections import deque
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['mydatabase']
nav_info = db['nav']

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
                        curr_qty = 0
                    else:
                        curr_qty -= remaining_qty
                        q.popleft()
        total_qty = 0
        average_price = 0
        for elem in q:
            total_qty += elem[1]
            average_price += elem[1]*elem[2]
        if total_qty == 0:
            return (0,0)
        average_price /= total_qty
        return (average_price, total_qty)
    

class UpdateNAVdata:
    
    def update_nav(self, username, latest_nav):
        q = deque()
        docs = nav_info.find({'client': username}).sort([('_id', 1)])
        for elem in docs:
            if elem['type'] == 'BUY':
                q.append(elem)     
        
        docs.rewind()        
        for elem in docs:
            if elem['type'] == 'SELL' and elem['checked'] == 0:
                nav_info.update_one({'_id':elem['_id']}, {'$set' : {'checked' : 1}})
                curr_qty = elem['qty']
                idx = 0
                while (curr_qty > 0 and idx < len(q)):
                    if (q[idx]['remaining_qty'] >= curr_qty):
                        remaining_qty = q[idx]['remaining_qty'] - curr_qty
                        qty = q[idx]['qty']
                        price = q[idx]['price']
                        curr_qty = 0
                        q[idx]['remaining_qty'] = remaining_qty
                        nav_info.update_one({'_id': q[idx]['_id']}, {'$set': {'remaining_qty': remaining_qty}})
                    else:
                        curr_qty -= q[idx]['remaining_qty']
                        q[idx]['qty'] = 0
                        nav_info.update_one({'_id': q[idx]['_id']}, {'$set': {'remaining_qty': 0}})
                    idx += 1

        print("Data Manipulated Successfully.")
        return 
            
        