import Node
import Protocol
from datetime import datetime


class Miner(Node):

    def __init__(self):
        self.hashRate = 0 # TODO: set by protocol class
        self.tempMemPool = [] # memPool that is going to be mined.


    # TODO: GetMempool():
    #  going to be run every iteration of the mine() loop. List of "transactions" its rerally just a list of lists in the format:
    #   [UID, senderID, RecieverID, Amouont, Fee]



    # make it so miners select from 10 - 15 transactions
    # make it so a miners hash rate updates every 5 blocks
    def mine(self):
        return
        # TODO: tempMemPool  = CreatesRandomMempool()
        # TODO: Random Nonce
        # TODO: Create Block(tempMempool, Nonce)
        # TODO: block.verify()
        # TODO: if true:
        # TODO:     post Block to GCP in "MINED BLOCK FIELD"
        # TODO:     initiate POW protocol for all nodes
