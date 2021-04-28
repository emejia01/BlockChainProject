
from hashlib import sha256
from random import randint


# Private method to generate hash
def generateHash(value):
    hashValue = sha256(value.encode("UTF-8")).hexdigest()
    return hashValue

# Method to find Nonce; Leading Zeros parameter to set difficulty
def calculateNonce(leadingZeros):
    currentNonce = 0
    while True:
        currentNonce += 1 # Random nonce value
        value = str(currentNonce)
        currentHash = generateHash(value)
        startingZeros = '0' * leadingZeros
        if currentHash.startswith(startingZeros):
            return currentNonce , currentHash

