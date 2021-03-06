#
# This file handles all the calls and acts a hub for which all our helper classes connect to.
# This class brings functionality to our project
#

from google.cloud import datastore

from BlockChainProject.Block import Block
from BlockChainProject.Node import Node
from BlockChainProject.Miner import Miner

from hashlib import sha256
from datetime import datetime
from time import sleep
from random import randint

import os

# Create OS environment variable for GCP Credential
os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/theomanavazian/Desktop/blockchainproject-311018-0932eb94714c.json"


# Class that makes all the magic happen, connect to GCP and talk to all the classes
class Protocol:

    # When we create a Protocol Object we want to update the mempool and the blockcahin.
    def __init__(self):
        self.createRandomMempool()
        self.getBlockChain()

    # Stores a copy of the blockchain
    Blockchain = []

    # Difficulty level for mining a mew block
    Difficulty = 1

    # sets the difficulty based on how long it took to mine the last 5 blocks
    def setDifficulty(self):
        # Time in seconds => 150 seconds is 2 mins, datetime subtraction returns time in seconds.
        self.Blockchain = self.getBlockChain()
        self.Difficulty *= 150 / (self.Blockchain[-5].time - self.Blockchain[-1].time)

    # Gets all nodes from the GCP stored as list of Node Objects (this list can include both Nodes and Miners)
    def getNodes(self):
        # Get Nodes from GCP
        client = datastore.Client()
        query = client.query(kind="Nodes")
        query.add_filter("isMiner", "=", False)
        results = list(query.fetch())

        # Format GCP data into Node Objects to return
        nodes = []
        for result in results:
            result = dict(result)
            FirstName, LastName, Email, UID, balance = result["FirstName"], result["LastName"], result["Email"], result[
                "UID"], result["balance"]
            currentNode = Node(FirstName=FirstName, LastName=LastName, Email=Email, UID=UID, balance=balance)

            nodes.append(currentNode)

        return nodes

    #  Gets all nodes from the GCP stored as list of Miner Objects
    @staticmethod
    def getMiners():
        # Get Miners from GCP
        client = datastore.Client()
        query = client.query(kind="Nodes")
        query.add_filter("isMiner", "=", True)
        results = list(query.fetch())

        # Format GCP data into Miner Objects to return
        miners = []
        for result in results:
            result = dict(result)
            FirstName, LastName, Email, UID, balance, hashRate, tempMemPool = result["FirstName"], result["LastName"], \
                                                                              result["Email"], result["UID"], result[
                                                                                  "balance"], result["hashRate"], \
                                                                              result["tempMemPool"]
            currentMiner = Miner(FirstName=FirstName, LastName=LastName, Email=Email, UID=UID, balance=balance)
            currentMiner.hashRate = hashRate
            currentMiner.tempMemPool = tempMemPool

            miners.append(currentMiner)

        return miners

    #  Gets all Blocks from the GCP stored as list of Block Objects
    def getBlockChain(self):
        # Get Blocks from GCP
        client = datastore.Client()
        query = client.query(kind="Blocks")
        query.order = ["num"]
        results = list(query.fetch())

        # Format GCP data into Block Objects to return
        blocks = []
        for result in results:
            result = dict(result)
            num, time, nonce, data, previousHash, currentHash = result["num"], result["time"], result["nonce"], result[
                "data"], result["previousHash"], result["currentHash"]
            currentBlock = Block(nonce, data, previousHash)  # TODO: change block counter
            currentBlock.num = num
            currentBlock.time = time
            currentBlock.currentHash = currentHash

            blocks.append(currentBlock)

        self.blockchain = blocks

    #  Gets all the Temporary Mined Blocks from the GCP stored as list of Blocks Objects
    #  OR grab Block with most transactions
    @staticmethod
    def getMinedBlock():
        # Get Blocks from GCP
        client = datastore.Client()
        query = client.query(kind="Mined Block")
        # query.order = ["-Transaction Count"]
        results = list(query.fetch())

        currentBlocks = []
        for result in results:
            # Format into Block Object
            result = dict(result)
            num, time, nonce, data, previousHash, currentHash = result["num"], result["time"], result["nonce"], result[
                "data"], result["previousHash"], result["currentHash"]
            currentBlock = Block(nonce, data, previousHash)  # TODO: change block counter
            currentBlock.num = num
            currentBlock.time = time
            currentBlock.currentHash = currentHash
            currentBlocks.append(currentBlock)

        return currentBlocks

    #  take data from theMinedBlock and remove the transactions from the GCP mempool
    @staticmethod
    def updateMempool(blockObj: Block):
        blockTransactions = blockObj.data.split(", ")
        client = datastore.Client()
        mempoolKeysToDelete = []

        # Result Format: [UID, senderID, RecieverID, Amount, Fee]

        for tempTrans in blockTransactions:  # results:
            transaction = tempTrans.split(',')
            # print("TRANSACTION: ", transaction)
            strTrans = transaction[0]
            strTrans = strTrans.replace("'", "")
            strTrans = strTrans.replace("[", "")
            print("---->", strTrans)
            key = client.key('Mempool', strTrans)
            mempoolKeysToDelete.append(key)
        # print(mempoolKeysToDelete)
        # Delete corresponding Transaction keys from the Mempool Table
        for key in mempoolKeysToDelete:
            client.delete(key)

    # Function that creates a transaction to be storerd in the mempoool.
    def Trasact(self, senderID, recieverID):

        transactionUID = sha256(str(datetime.now()).encode("UTF-8")).hexdigest()
        client = datastore.Client()
        key = client.key('Mempool', transactionUID)
        entity = datastore.Entity(key=key)
        entity.update({
            "UID": transactionUID,
            "senderID": senderID,
            "recieverID": recieverID,
            "amount": 1,
            "fee": .02,
            "data": str(transactionUID) + "," + str(senderID) + "," + str(recieverID) + "," + str(1) + "," + str(.02)
        })
        client.put(entity)
        self.getMempool()

    #  Adds the mined block to the end of the blockchain
    #  delete all temp Mined blocks
    def addBlock(self, blockObj: Block):
        # Add Block to GCP
        client = datastore.Client()
        key = client.key('Blocks', blockObj.currentHash)
        entity = datastore.Entity(key=key)
        entity.update({
            "currentHash": blockObj.currentHash,
            "data": str(blockObj.data),
            "nonce": blockObj.nonce,
            "num": blockObj.num,
            "previousHash": blockObj.previousHash,
            "time": blockObj.time
        })
        client.put(entity)
        # Clear all data from Mined Blocks Table
        query = client.query(kind="Mined Block")
        results = list(query.fetch())

        for result in results:
            client.delete(result.key)  # TODO: Test this line

        print("Block Successfully Mined")
        self.getMempool()

    # Adds a "Candidate Block". this is just a block that has been mined but hasnt been added to the Blockchain yet.
    # once the candidate block get verified, it gets added to the blockchain
    def addMinedBlock(self, blockObj: Block):
        # Add Block to GCP
        client = datastore.Client()
        key = client.key('Mined Block', blockObj.currentHash)
        entity = datastore.Entity(key=key)
        entity.update({
            "currentHash": blockObj.currentHash,
            "data": str(blockObj.data),
            "nonce": blockObj.nonce,
            "num": blockObj.num,
            "previousHash": blockObj.previousHash,
            "time": blockObj.time
        })
        client.put(entity)

    # Refreses the current mempool so the miner akways has the most up to date version of it
    def getMempool(self):
        # get all transactions from Mempool table in GCP
        self.getBlockChain()
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
            currentTransaction = str(transactionUID) + "," + senderUID + "," + recieverID + "," + str(
                transactionAmount) + "," + str(fee)
            allTransactions.append(currentTransaction)

        self.MEMPOOL = allTransactions

    # Creates temp mempool for the miner, of random size of 3 - 5 transactions
    def createRandomMempool(self):
        self.getMempool()
        if len(self.MEMPOOL) < 3:
            self.tempMempool = self.MEMPOOL

        randomSize = randint(3, 5)
        if len(self.MEMPOOL) < randomSize:
            self.tempMempool = self.MEMPOOL
        else:
            self.tempMempool = self.MEMPOOL[:randomSize]

    # This is the function that actuall mines based on the current mempool and hash rate etc. Takes Miner Object as a paramater
    def mine(self, m):
        nonce = 1

        while True:
            if len(self.tempMempool) == 0:
                sleep(10)
                self.createRandomMempool()

                continue

            if nonce == m.hashRate:
                nonce = 1
                self.createRandomMempool()
                sleep(1)

            self.blockchain = Node.getBlockChain()
            blockNum = len(Node.getBlockChain())
            time = datetime.now()
            data = self.tempMempool
            prevHash = self.blockchain[-1].previousHash

            newBlock = Block(data=data, previousHash=prevHash, nonce=nonce)
            newBlock.time = time
            newBlock.num = blockNum
            newBlock.previousHash = self.blockchain[-1].currentHash
            newBlock.getCurrentHash()
            print("Generating Hash...: ", newBlock.currentHash)

            if Node.verify(newBlock, m.UID):
                self.addMinedBlock(newBlock)
                self.POW()
                self.createRandomMempool()
                sleep(2)

            nonce += 1

        return

    # Updates all the account balances of the Nodes, called when a new block is added to the blockchain.
    def updateBalances(self, block):
        blockTransactions = block.data.split(", ")

        for tempTrans in blockTransactions:
            transaction = tempTrans.split(',')
            strTrans1 = transaction[1]
            strTrans1 = strTrans1.replace("'", "")
            strTrans1 = strTrans1.replace("[", "")

            client = datastore.Client()

            with client.transaction():
                key = client.key("Nodes", strTrans1)
                entity = client.get(key)
                entity['balance'] = str(int(entity['balance']) - 1)
                client.put(entity)

        counter = 0
        counter2 = 0
        for tempTrans in blockTransactions:
            transaction = tempTrans.split(',')
            strTrans2 = transaction[2]
            strTrans2 = strTrans2.replace("'", "")
            strTrans2 = strTrans2.replace("[", "")

            if strTrans2 == '15b8ec7d599c752a65a324c25558be720a3db5a7f80d20a7340baaa8bb21f64d':
                counter += 1
            else:
                counter2 += 1

        client = datastore.Client()

        with client.transaction():
            # these keys are hard coded to the accounts of BITCOIN and ETHEREUM.
            # The reason for this is this is the only campaign we have running currently. a real world application would
            # Implement this differently, but for now this works just as well because this address will never change
            key2 = client.key("Nodes", '15b8ec7d599c752a65a324c25558be720a3db5a7f80d20a7340baaa8bb21f64d')
            entity2 = client.get(key2)
            entity2['balance'] = int(entity2['balance']) + counter

            client.put(entity2)

        client = datastore.Client()

        with client.transaction():

            key3 = client.key("Nodes", '124d0d8d47c3f4eddfa27c8004057d9f57fe52b76ec7e6c2c27d7c570ef984c1')
            entity3 = client.get(key3)
            entity3['balance'] = int(entity3['balance']) + counter2

            client.put(entity3)

    # returns a boolean to see if a list of transactions are still in the mempool
    # we use this to handdle concurrent mining so that votes doont get cuonted twice.
    def transStillInMempool(self, block):
        # get all transactions from Mempool table in GCP
        client = datastore.Client()
        query = client.query(kind="Mempool")
        results = list(query.fetch())

        tempMEMUIDS = []
        for result in results:
            result = dict(result)
            data = result["data"]

            data = data.split(", ")
            for i in data:
                transaction = i.replace("'", "")
                transaction = transaction.replace("[", "")
                temp = transaction.split(',')
                tempUID = temp[0]
                tempMEMUIDS.append(tempUID)

        transUIDS = block.data.split(", ")
        for i in transUIDS:
            transaction = i.replace("'", "")
            transaction = transaction.replace("[", "")
            temp = transaction.split(',')
            tempUID = temp[0]

            if tempUID not in tempMEMUIDS:
                return False

        return True

    # Proof of work, just calls verify on all the nodes and handles adding the block
    def POW(self):
        counter = 0
        self.Nodes = self.getNodes()
        blocks = self.getMinedBlock()

        try:
            block = blocks[0]
        except:
            print("Block not added, Block already mined")
            return False
        for currentBlock in blocks:
            if len(currentBlock.data) > len(block.data):
                block = currentBlock

        for node in self.Nodes:
            if node.verify(block, node.UID):
                counter += 1
            if counter == len(self.Nodes) // 2:
                if self.transStillInMempool(block):
                    self.addBlock(block)
                    self.updateMempool(block)
                    self.updateBalances(block)
                    return True

                else:
                    self.createRandomMempool()
                    print("Block not added, Block already mined")

                    return False
        return False

