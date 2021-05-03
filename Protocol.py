from google.cloud import datastore
from BlockChainProject.Node import Node
from BlockChainProject.Miner import Miner
from BlockChainProject.Block import *
import os

# Create OS environment variable for GCP Credential
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/erikmejia/Desktop/blockchainproject-311018-0932eb94714c.json"

# Class that makes all the magic happen, connect to GCP and talk to all the classes
class Protocol:

    # Stores all the nodes that are on the Network
    Nodes = []  # TODO: List of nodes pulled from GCP

    # Stores a copy of the blockchain
    Blockchain = [] # TODO: Pull from GCP

    # Difficulty should be updated every 5 blocks -> ~ 2.5 minutes
    # also change the hashrate for all the miners
    Difficulty = 1  # TODO: CALCULATE from TOTALHahsrate and post to GCP

    # The Total Network Hashrate, Honestly this field doesnt really do anything, its more for show.
    TotalNetworkHashRate = 0  # TODO: calculate total NetworkHashRate every 5 blocks, then update field on GCP

    # Theory is we want 5 blocks ever 2.5 minutes which means we want to mine a block every 30 seconds
    # if we take the time stamp for block i and subtract it from i-5 the number should be around 2.5 minutes.
    # if this is not true we do difficulty *= "2.5 minutes" / <the time it actually took>
    def setDifficulty(self):
        # Time in seconds => 150 seconds is 2 mins, datetime subtraction returns time in seconds.
        self.Difficulty *= 150 / (self.Blockchain[-5].time - self.Blockchain[-1].time)
        # TODO: post difficulty to GCP



    def POW(self):
        counter = 0
        for node in self.Nodes:
            if node.verify():
                counter += 1
            if counter == len(self.Nodes) // 2:
                return True
        return False


    # Gets all nodes from the GCP stored as list of Node Objects (this list can include both Nodes and Miners)
    @staticmethod
    def getNodes():
        # Get Nodes from GCP
        client = datastore.Client()
        query = client.query(kind="Nodes")
        query.add_filter("isMiner", "=", False)
        results = list(query.fetch())

        # Format GCP data into Node Objects to return
        nodes = []
        for result in results:
            result = dict(result)
            FirstName, LastName, Email, UID, balance = result["FirstName"], result["LastName"], result["Email"], result["UID"], result["balance"]
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
            FirstName, LastName, Email, UID, balance, hashRate, tempMemPool = result["FirstName"], result["LastName"], result["Email"], result["UID"], result["balance"], result["hashRate"], result["tempMemPool"]
            currentMiner = Miner(FirstName=FirstName, LastName=LastName, Email=Email, UID=UID, balance=balance)
            currentMiner.hashRate = hashRate
            currentMiner.tempMemPool = tempMemPool

            miners.append(currentMiner)

        return miners

    #  Gets all Blocks from the GCP stored as list of Block Objects
    @staticmethod
    def getBlockChain():
        # Get Blocks from GCP
        client = datastore.Client()
        query = client.query(kind="Blocks")
        results = list(query.fetch())

        # Format GCP data into Block Objects to return
        blocks = []
        for result in results:
            result = dict(result)
            num, time, nonce, data, previousHash, currentHash = result["num"], result["time"], result["nonce"], result["data"], result["previousHash"], result["currentHash"]
            currentBlock = Block(nonce, data, previousHash) # TODO: change block counter
            currentBlock.num = num
            currentBlock.time = time
            currentBlock.currentHash = currentHash

            blocks.append(currentBlock)

        return blocks

    #  Gets all the Temporary Mined Blocks from the GCP stored as list of Blocks Objects
    #  OR grab Block with most transactions
    @staticmethod
    def getMinedBlock():
        # Get Blocks from GCP
        client = datastore.Client()
        query = client.query(kind="Mined Block")
        query.order = ["-Transaction Count"]
        result = list(query.fetch(limit=1))[0]

        # Format into Block Object
        result = dict(result)
        num, time, nonce, data, previousHash, currentHash = result["Num"], result["Time"], result["Nonce"], result["Data"], result["Previous Hash"], result["Current Hash"]
        currentBlock = Block(nonce, data, previousHash)  # TODO: change block counter
        currentBlock.num = num
        currentBlock.time = time
        currentBlock.currentHash = currentHash

        return currentBlock

    #  Adds the mined block to the end of the blockchain
    #  delete all temp Mined blocks
    @staticmethod
    def addMinedBlock(blockObj: Block):
        # Add Block to GCP
        client = datastore.Client()
        key = client.key('Blocks', blockObj.num)
        entity = datastore.Entity(key=key)
        entity.update({
            "currentHash": blockObj.currentHash,
            "data": blockObj.data,
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

    #  take data from theMinedBlock and remove the transactions from the GCP mempool
    @staticmethod
    def updateMempool(blockObj: Block):
        blockTransactions = blockObj.data
        client = datastore.Client()
        mempoolKeysToDelete = set()

        # Result Format: [UID, senderID, RecieverID, Amount, Fee]
        for transaction in blockTransactions: #results:
            key = client.key('Mempool', transaction[0])
            mempoolKeysToDelete.add(key)

        # Delete corresponding Transaction keys from the Mempool Table
        for key in mempoolKeysToDelete:
            client.delete(key)
