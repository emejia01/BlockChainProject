from datetime import datetime
from hashlib import sha256

# Class for individual Blocks(nodes) within the Blockchain
class Block:
    num = 0
    # Create Data fields for each Block object
    def __init__(self, nonce, data, previousHash):
        self.num = Block.num
        self.time = datetime.now()
        self.nonce = nonce
        self.data = data
        self.previousHash = previousHash
        self.currentHash = None

    def getCurrentHash(self):
        hashString = ''
        hashString += str(self.num)
        hashString += str(self.time)
        hashString += str(self.nonce)
        hashString += str(self.data)
        hashString += str(self.previousHash)
        self.currentHash = sha256(hashString.encode("UTF-8")).hexdigest()