
from pymongo import MongoClient

class clientLinkClass:
    def clientLink(self, kill):
        if kill:
            client = MongoClient(host='rouge-data', port=27017)
        else:
            client = MongoClient(host='localhost', port=27017)
        
        return client
