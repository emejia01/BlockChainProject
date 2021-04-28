import Node
import Protocol
from datetime import datetime


class Miner(Node):

    def __init__(self):
        self.hashRate = 0 # TODO: set by protocol class
        self.tempMemPool = [] # memPool that is going to be mined.

    def mine(self):
        return
        # TODO: tempMemPool  = CreatesRandomMempool()
        # TODO: Random Nonce
        # TODO: Create Block(tempMempool, Nonce)
        # TODO: block.verify()
        # TODO: if true:
        # TODO:     post Block to GCP in "MINED BLOCK FIELD"
        # TODO:     initiate POW protocol for all nodes
