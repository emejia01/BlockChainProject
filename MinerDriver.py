from BlockChainProject.Miner import Miner
from BlockChainProject.Protocol import Protocol


m = Miner()
m.hashRate = 100000
protocol = Protocol()

protocol.mine(m)


# TODO: PRINT MEMPOOL AFTER MINING TO SEE WHY TRANSACTIONS ARE STILL SHOWING UP WHEN THEY ARENT IN MEMPOOL
# TODO: MAKE BLOCK POINT TO PREV HASH --> SHOULD BE EASY.