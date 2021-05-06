from BlockChainProject.Miner import Miner

m = Miner()
m.hashRate = 100000
m.mine()

#from BlockChainProject.Protocol import Protocol
#from BlockChainProject.Block import Block

#x = Block(data="2111", nonce="99",previousHash="123")
#x.num = 1
#Protocol.addMinedBlock(x)
