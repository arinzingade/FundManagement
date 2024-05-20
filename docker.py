
from pymongo import MongoClient
import certifi
import ssl


class clientLinkClass:
    def clientLink(self, kill):
        if kill:  
            client = MongoClient("mongodb+srv://arinzingade29:eqoRi2aDw5sI8Xl0@rouge-cluster.lpw9amw.mongodb.net/?retryWrites=true&w=majority&appName=rouge-cluster")
        else:
            client = MongoClient(host='localhost', port=27017)
        
        return client
