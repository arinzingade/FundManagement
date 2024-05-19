
from pymongo import MongoClient
import certifi
import ssl

ca_cert = certifi.where()

class clientLinkClass:
    def clientLink(self, kill):
        if kill:
            ssl_context = ssl.create_default_context(cafile=ca_cert)
            ssl_context.check_hostname = False  
            ssl_context.verify_mode = ssl.CERT_NONE 
            
       
            client = MongoClient("mongodb+srv://arinzingade29:eqoRi2aDw5sI8Xl0@rouge-cluster.lpw9amw.mongodb.net/?retryWrites=true&w=majority&appName=rouge-cluster", 
                                 tls=True, tlsAllowInvalidCertificates=True)
        else:
            client = MongoClient(host='localhost', port=27017)
        
        return client
