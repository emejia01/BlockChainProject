from BlockChainProject.Node import Node
from google.cloud import datastore
from datetime import datetime
from time import sleep
from hashlib import sha256
from random import randint
from BlockChainProject.Blockchain import Block
from BlockChainProject.Protocol import Protocol
from BlockChainProject.Node import Node


# Create OS environment variable for GCP Credential

class Miner():

    def __init__(self, UID=sha256(str(datetime.now()).encode("UTF-8")).hexdigest()):#,FirstName, LastName, Email, UID=sha256(str(datetime.now()).encode("UTF-8")).hexdigest(), balance=10):
        #super(Miner, self).__init__(FirstName, LastName, Email, UID, balance)
        self.hashRate = 0 # TODO: set by protocol class
        self.tempMemPool = [] # memPool that is going to be mined.
        self.UID = UID
        self.balance = 0
        self.blockchain = Protocol.getBlockChain()
        self.allTransactions = self.getMempool()
        #super(Miner, self).__init__(FirstName, LastName, Email, UID, balance)

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
            fee = result["fee"]
            currentTransaction = str(transactionUID) + "," + senderUID + "," + recieverID + "," + str(transactionAmount) + "," + str(fee)
            allTransactions.append(currentTransaction)

        return allTransactions

    # Creates temp mempool of random size of 10 - 15 transactions
    def createRandomMempool(self):

        if len(self.allTransactions) < 10:
            return self.allTransactions

        randomSize = randint(3, 5)
        if len(self.allTransactions) < randomSize:
            return self.allTransactions
        else:
            return self.allTransactions[:randomSize]

    # make it so a miners hash rate updates every 5 blocks
    def mine(self):

        nonce = 1
        self.tempMempool = self.createRandomMempool()

        while True:
            if len(self.tempMempool) == 0:
                sleep(10)
                continue

            if nonce == self.hashRate:
                nonce = 1
                self.tempMempool = self.createRandomMempool()
                sleep(1)

            self.blockchain = Protocol.getBlockChain()
            blockNum = len(Protocol.getBlockChain())
            time = datetime.now()
            data = self.tempMempool
            prevHash = self.blockchain[-1].previousHash

            newBlock = Block(data=data, previousHash=prevHash, nonce=nonce)
            newBlock.time = time
            newBlock.num = blockNum
            newBlock.getCurrentHash()
            print(newBlock.currentHash)

            if Node.verify(newBlock, self.UID):
                self.tempMempool = self.createRandomMempool()
                Protocol.addMinedBlock(newBlock)
                protocol = Protocol() # TODO: Static method maybe??
                protocol.POW()

            nonce += 1

        return
