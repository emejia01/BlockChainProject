from hashlib import sha256
#from BlockChainProject.Protocol import *
from datetime import datetime
from google.cloud import datastore
import os

# Create OS environment variable for GCP Credential
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/erikmejia/Desktop/blockchainproject-311018-0932eb94714c.json"


class Node:

    def __init__(self, FirstName, LastName, Email, UID=sha256(str(datetime.now()).encode("UTF-8")).hexdigest(), balance=10):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Email = Email
        self.UID = UID
        self.balance = 0
        self.Blockchain = [] # TODO: Pull from GCP


    def verify(self, block):
        hashString = ''
        hashString += block.num
        hashString += block.time
        hashString += block.nonce
        hashString += block.ledger
        hashString += block.previousHash
        hashed = sha256(hashString.encode("UTF-8")).hexdigest()

        if hashed.startswith('0' * Protocol.Difficulty):
            return True
        return False

    # Add transaction to Mempool
    def Trasact(self, recieverID):

        transactionUID = sha256(str(datetime.now()).encode("UTF-8")).hexdigest()
        client = datastore.Client()
        key = client.key('Mempool', transactionUID)
        entity = datastore.Entity(key=key)
        entity.update({
            "UID": transactionUID,
            "senderID": self.UID,
            "recieverID": recieverID,
            "amount": self.balance,
            #"fee": blockObj.previousHash,
            "data": [transactionUID, self.UID, recieverID, self.balance]
        })
        client.put(entity)

        # Update Node balance
        self.balance = 0
