from BlockChainProject.Node import Node
from google.cloud import datastore
from datetime import datetime
from hashlib import sha256
from random import randint
import os

# Create OS environment variable for GCP Credential
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/erikmejia/Desktop/blockchainproject-311018-0932eb94714c.json"

class Miner(Node):

    def __init__(self,FirstName, LastName, Email, UID=sha256(str(datetime.now()).encode("UTF-8")).hexdigest(), balance=10):
        self.hashRate = 0 # TODO: set by protocol class
        self.tempMemPool = [] # memPool that is going to be mined.
        super(Miner, self).__init__(FirstName, LastName, Email, UID, balance)

    # [transactionUID, self.UID, recieverID, self.balance]
    def getMempool(self):
        # get all transactions from Mempool table in GCP
        client = datastore.Client()
        query = client.query(kind="Mempool")
        results = list(query.fetch())

        allTransactions = []
        for result in results:
            result = dict(result)
            transactionUID = result["UID"]
            senderUID = result["senderID"]
            recieverID = result["recieverID"]
            transactionAmount = result["amount"]

            currentTransaction = [transactionUID, senderUID, recieverID, transactionAmount]
            allTransactions.append(currentTransaction)

        return allTransactions

    # Creates temp mempool of random size of 10 - 15 transactions
    def createRandomMempool(self):
        allTransactions = self.getMempool()
        if len(allTransactions) < 10:
            return allTransactions

        randomSize = randint(10, 15)
        if len(allTransactions) < randomSize:
            return allTransactions
        else:
            return allTransactions[:randomSize]

    # make it so a miners hash rate updates every 5 blocks
    def mine(self):
        return
        # TODO: tempMemPool  = CreatesRandomMempool(self.mempool)
        # TODO: Random Nonce
        # TODO: Create Block(tempMempool, Nonce)
        # TODO: block.verify()
        # TODO: if true:
        # TODO:     post Block to GCP in "MINED BLOCK FIELD"
        # TODO:     initiate POW protocol for all nodes
