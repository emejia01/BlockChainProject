# Class that makes all the magic happen, connect to GCP and talk to all the classes
class Protocol:

    # Stores all the nodes that are on the Network
    Nodes = []  # TODO: List of nodes pulled from GCP

    # Stores a copy of the blockchain
    Blockchain = [] # TODO: Pull from GCP

    # Difficulty should be updated every 5 blocks -> ~ 2.5 minutes
    # also change the hashrate for all the miners
    Difficulty = 1  # TODO: CALCULATE from TOTALHahsrate and post to GCP

    # The Total Network Hashrate, Honestly this field doesnt really do anything, its more for show.
    TotalNetworkHashRate = 0  # TODO: calculate total NetworkHashRate every 5 blocks, then update field on GCP

    # Theory is we want 5 blocks ever 2.5 minutes which means we want to mine a block every 30 seconds
    # if we take the time stamp for block i and subtract it from i-5 the number should be around 2.5 minutes.
    # if this is not true we do difficulty *= "2.5 minutes" / <the time it actually took>
    def setDifficulty(self):
        # Time in seconds => 150 seconds is 2 mins, datetime subtraction returns time in seconds.
        self.Difficulty *= 150 / (self.Blockchain[-5].time - self.Blockchain[-1].time)



    def POW(self):
        counter = 0
        for node in self.Nodes:
            if node.verify():
                counter += 1
            if counter == len(self.Nodes) // 2:
                return True
        return False




