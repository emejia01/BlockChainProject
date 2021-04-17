from random import randint
from hashlib import sha256


# Class for individual Blocks(nodes) within the Blockchain
class Block:

    # Create Data fields for each Block object
    def __init__(self, previousHash="0000000000", data=""):
        self.previousHash = previousHash
        self.data = data
        self.nonce = self.calculateNonce(2) # 2 leading zeros difficulty
        self.currentHash = self.calculateHash()
        self.nextBlock = None

    # Method to find Nonce; Leading Zeros parameter to set difficulty
    def calculateNonce(self, leadingZeros):
        while True:
            currentNonce = str(randint(0, 1000000)) # Random nonce value
            value = self.previousHash + self.data + currentNonce
            currentHash = self._generateHash(value)
            startingZeros = '0' * leadingZeros
            if currentHash.startswith(startingZeros):
                return currentNonce

    # Method to calculate hash of block data fields
    def calculateHash(self):
        value = self.previousHash + self.data + self.nonce
        return self._generateHash(value)

    # Private method to generate hash
    def _generateHash(self, value):
        hashValue = sha256(value.encode("UTF-8")).hexdigest()
        return hashValue

