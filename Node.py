from hashlib import sha256
from Protocol import *
from datetime import datetime



class Node:

    def __init__(self, FirstName, LastName, Email):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Email = Email
        self.UID = sha256(datetime.now().encode("UTF-8")).hexdigest()
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

    # TODO: Trasact():
    #  add transaction to Mempool
    #   [UID, senderID, RecieverID, Amouont, Fee]

