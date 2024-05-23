
from collections import deque
from pymongo import MongoClient

from docker import clientLinkClass


ck = clientLinkClass()
client = ck.clientLink(True)

db = client['mydatabase']
nav_info = db['nav']
transaction_info = db['transactions']

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
        return (round(average_price,2), round(total_qty,2))
    

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
                sold_price = 0
                counter_qty = 0
                realised = 0
                
                while (curr_qty > 0 and idx < len(q)):
                    if (q[idx]['remaining_qty'] >= curr_qty):
                        remaining_qty = q[idx]['remaining_qty'] - curr_qty
                        counter_qty += curr_qty
                        sold_price += q[idx]['price']*curr_qty
                        print("Curr qty: ", curr_qty)
                        realised += curr_qty*(latest_nav - q[idx]['price'])
                        print("realised 1: ", realised)
                        curr_qty = 0
                        q[idx]['remaining_qty'] = remaining_qty
                        nav_info.update_one({'_id': q[idx]['_id']}, {'$set': {'remaining_qty': round(remaining_qty,2)}})
                    
                    elif (q[idx]['remaining_qty'] != 0):
                        curr_qty -= q[idx]['remaining_qty']
                        counter_qty += q[idx]['qty']
                        sold_price += q[idx]['price']*q[idx]['qty']
                        realised += q[idx]['remaining_qty']*(latest_nav - q[idx]['price'])
                        print("realised 2: ", realised)
                        q[idx]['qty'] = 0
                        nav_info.update_one({'_id': q[idx]['_id']}, {'$set': {'remaining_qty': 0}})
                        
                    idx += 1
                
                sold_price /= counter_qty
                nav_info.update_one({'_id':elem['_id']}, {'$set' : {'sold_at' : sold_price}})
                nav_info.update_one({'_id':elem['_id']}, {'$set' : {'realised' : round(realised,2)}})
                
        
        docs.rewind()
        total_unrealised = 0
        total_realised = 0
        for elem in docs:
            if elem['type'] == 'BUY' and elem['client'] == username:
                print(latest_nav)
                remaining = elem['remaining_qty']
                price = elem['price']
                unrealised = remaining*(latest_nav - price)
                nav_info.update_one({'_id':elem['_id']}, {'$set' : {'unrealised' : round(unrealised,2)}})
                
                total_unrealised += elem['unrealised']
            
            if elem['type'] == 'SELL' and elem['client'] == username:
                total_realised += elem['realised']
            
        return [round(total_unrealised,2), round(total_realised,2)]
            

class NumberConv:
    
    def numConv(self, num, flag):
        crore = 10000000
        lakhs = 100000
        thousands = 1000
        
        if flag == 0:
            if num >= crore:
                return str(round(num / crore,2)) + ' Cr'
            if num >= lakhs:
                return str(round(num / lakhs,2)) + ' L'
            if num >= thousands:
                return str(round(num / thousands,2)) + ' K'
        
        if flag == 1:
            if num >= crore:
                return str(round(num / crore,2)) + ' Crore'
            if num >= lakhs:
                return str(round(num / lakhs,2)) + ' Lakhs'
            if num >= thousands:
                return str(round(num / thousands,2)) + ' Thousand'

class TotalInvested:
    
    def __init__(self, transaction_info, username):
        self.transaction_info = transaction_info
        self.username = username
        self.transactionData = transaction_info.find({'client': username})
    
    def total_invested(self):
        total_invested = 0
        for elem in self.transactionData:
            if elem['particular'] == 'DEPOSIT':
                total_invested += elem['credit']
            elif elem['particular'] == 'WITHDRAW':
                total_invested -= elem['debit']
        
        return total_invested



