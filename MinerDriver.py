from BlockChainProject.Miner import Miner
from BlockChainProject.Protocol import Protocol


m = Miner()
m.hashRate = 100000
protocol = Protocol()




protocol.mine(m)

