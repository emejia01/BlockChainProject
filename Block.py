from datetime import datetime

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


