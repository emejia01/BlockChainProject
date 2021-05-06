from BlockChainProject.Block import Block
from BlockChainProject.Protocol import Protocol


B = Block(nonce="100", data="THIS IS THE GENESIS BLOCK", previousHash="None")
B.getCurrentHash()


Protocol.addBlock(B)

#update mempool anytime a transaction has been made
#update mempool anytime a miner mined a block
