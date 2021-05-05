from hashlib import sha256
from datetime import datetime
from google.cloud import datastore
import os

# Create OS environment variable for GCP Credential
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/erikmejia/Desktop/blockchainproject-311018-0932eb94714c.json"


class Node:

    def __init__(self, FirstName ='', LastName='', Email='', UID=sha256(str(datetime.now()).encode("UTF-8")).hexdigest(),balance = 1):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Email = Email
        self.UID = UID
        self.balance = balance
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
            "amount": 1,
            "fee": .02,
            "data": [transactionUID, self.UID, recieverID, 1, .02]
        })
        client.put(entity)

        # Update Node balance
        #self.balance = 0 # we update only when the block that has this transaction is mined
    def toString(self):
        print("NODE:")
        print('FirstName', self.FirstName)
        print('LastName', self.LastName)
        print('Email', self.Email)
        print('UID', self.UID)
        print('Bal',self.balance)




#keep here
from BlockChainProject.Protocol import *
