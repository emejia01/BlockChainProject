from Block import *

# Chain Structure to hold sequence of Blocks(nodes)
class Blockchain:

    # Create data fields for Blockchain object
    def __init__(self, genesisHash="0000000000", genesisData=""):
        self.genesisBlock = Block(genesisHash, genesisData)
        self.allBlocks = [self.genesisBlock]
        self.currentBlock = self.allBlocks[-1]

    # Method to add block to chain (using Block object)
    def addBlock(self, data):
        previousHash = self.currentBlock.currentHash
        newBlock = Block(previousHash=previousHash, data=data)
        self.currentBlock.nextBlock = newBlock
        self.allBlocks.append(newBlock)
        self.currentBlock = self.allBlocks[-1]

