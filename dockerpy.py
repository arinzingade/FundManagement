from pymongo import MongoClient
import certifi
from pymongo.server_api import ServerApi


class clientLinkClass:
    def clientLink(self, kill):
        uri = "mongodb://arinzingade29:Napobose01@ac-phzatpb-shard-00-00.lpw9amw.mongodb.net:27017,ac-phzatpb-shard-00-01.lpw9amw.mongodb.net:27017,ac-phzatpb-shard-00-02.lpw9amw.mongodb.net:27017/?ssl=true&replicaSet=atlas-rdvyyi-shard-0&authSource=admin&retryWrites=true&w=majority&appName=rouge-cluster"
        if kill:
            client = MongoClient(uri, server_api = ServerApi('1'))
        else:
            client = MongoClient(host='localhost', port=27017)
        
        return client

# Usage example
clientLink = clientLinkClass()
client = clientLink.clientLink(True)
