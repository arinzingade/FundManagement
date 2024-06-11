from pymongo import MongoClient
import certifi

class clientLinkClass:
    def clientLink(self, kill):
        if kill:
            client = MongoClient(
                "mongodb+srv://arinzingade29:Napobose01@rouge-cluster.lpw9amw.mongodb.net/",
                tlsCAFile=certifi.where()
            )
        else:
            client = MongoClient(host='localhost', port=27017)
        
        return client

# Usage example
clientLink = clientLinkClass()
client = clientLink.clientLink(True)
