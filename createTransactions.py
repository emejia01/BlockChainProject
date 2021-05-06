from datetime import datetime
from google.cloud import datastore
from hashlib import sha256
from BlockChainProject.Node import Node
from random import randint

import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/erikmejia/Desktop/blockchainproject-311018-0932eb94714c.json"

client = datastore.Client()

for i in range(20):
    print("added")
    currentNode = Node()
    randomSenderAddress = randint(0, 99999999999)
    currentNode.Trasact("101010101010")


