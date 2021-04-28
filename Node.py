from hashlib import sha256
from Protocol import *


class Node:

    COUNTER = 0

    def __init__(self):
        self.UID = sha256(Node.COUNTER.encode("UTF-8")).hexdigest()
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

        # self.hashRate = 0 # TODO: set by protocol class
        # self.tempMemPool = [] # List of transactions made by this user
