from datetime import datetime
from hashlib import sha256
from BlockChainProject.Node import Node


# Create OS environment variable for GCP Credential

class Miner():
    def __init__(self, UID=sha256(str(datetime.now()).encode("UTF-8")).hexdigest()):#,FirstName, LastName, Email, UID=sha256(str(datetime.now()).encode("UTF-8")).hexdigest(), balance=10):
        #super(Miner, self).__init__(FirstName, LastName, Email, UID, balance)
        self.hashRate = 0 # TODO: set by protocol class
        self.tempMemPool = [] # memPool that is going to be mined.
        self.UID = UID
        self.balance = 0
        self.blockchain = Node.getBlockChain()
        #super(Miner, self).__init__(FirstName, LastName, Email, UID, balance)






