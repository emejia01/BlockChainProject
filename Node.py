#Node class defines all the attributes of a Node (Voter account)

from hashlib import sha256
from datetime import datetime
from google.cloud import datastore
from BlockChainProject.Block import Block

import os


# Create OS environment variable for GCP Credential
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/theomanavazian/Desktop/blockchainproject-311018-0932eb94714c.json"


class Node:

    def __init__(self, FirstName ='', LastName='', Email='', UID=sha256(str(datetime.now()).encode("UTF-8")).hexdigest(),balance = 1):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Email = Email
        self.UID = UID
        self.balance = balance
        self.Blockchain = self.getBlockChain() # TODO: Pull from GCP


    @staticmethod
    # Each node has a verify method which gets called when a new block is trying to be mined
    def verify(block, UID):

        if block.currentHash.startswith('0' * 1):
            print(str(UID) + " Verified Block")
            return True
        return False



        # Update Node balance
        #self.balance = 0 # we update only when the block that has this transaction is mined
    def toString(self):
        print("NODE:")
        print('FirstName', self.FirstName)
        print('LastName', self.LastName)
        print('Email', self.Email)
        print('UID', self.UID)
        print('Bal',self.balance)


    @staticmethod
    # returns the current blockchain for each node to store it
    def getBlockChain():
        # Get Blocks from GCP
        client = datastore.Client()
        query = client.query(kind="Blocks")
        query.order = ["time"]
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