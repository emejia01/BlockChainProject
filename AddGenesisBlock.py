# simple driver program that just creates the Genesis Block

from BlockChainProject.Block import Block
from BlockChainProject.Protocol import Protocol


B = Block(nonce="100", data="THIS IS THE GENESIS BLOCK", previousHash="None")
B.getCurrentHash()

Protocol.addBlock(B)

