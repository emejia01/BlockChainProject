# This file is a test file, we use it as a driver to quickly create 21 transactions to test the functionality of our Blockchain

from datetime import datetime
from google.cloud import datastore
from hashlib import sha256
from BlockChainProject.Protocol import Protocol
from random import randint


import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/theomanavazian/Desktop/blockchainproject-311018-0932eb94714c.json"

client = datastore.Client()
p = Protocol()

# creates 21 transactions
for i in range(3):
    p.Trasact('230dfcc1626f38aab15c4dc6b866844f616c5346d0b4c0c1af40c75edc772ded', "15b8ec7d599c752a65a324c25558be720a3db5a7f80d20a7340baaa8bb21f64d")
    p.Trasact('38773e6fde3457d0ecd9db2efda31f9bebf3e9a2a6e9afc3565c29a96b1334d2', "15b8ec7d599c752a65a324c25558be720a3db5a7f80d20a7340baaa8bb21f64d")
    p.Trasact('45c801a925fe4dd7207dd357441ed25bdbdc27adfade11dc890b8f4a64c8caa0', "15b8ec7d599c752a65a324c25558be720a3db5a7f80d20a7340baaa8bb21f64d")
    p.Trasact('81f2b42126b8c7b2cc30c40b005012bd1849a1ac349f0507164adf9dd235b3e9', "15b8ec7d599c752a65a324c25558be720a3db5a7f80d20a7340baaa8bb21f64d")
    p.Trasact('b9ea90b6a4af2cd4a454fae643761aa90dc68d00e53b2b2868a6e60e2df61102', "15b8ec7d599c752a65a324c25558be720a3db5a7f80d20a7340baaa8bb21f64d")
    p.Trasact('c4deaa12046289fe2d15ff228adab9d8897ce72c3eb8f9e7a2f826b32792ef91', "124d0d8d47c3f4eddfa27c8004057d9f57fe52b76ec7e6c2c27d7c570ef984c1")
    p.Trasact('ee09d3d5816205fc4e7ced6a88787d210ffe189c5080d6fdd05b476c26d1e08e', "124d0d8d47c3f4eddfa27c8004057d9f57fe52b76ec7e6c2c27d7c570ef984c1")


