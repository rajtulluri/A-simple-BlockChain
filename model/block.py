from datetime import datetime
import json
import hashlib

class Block:
    """
    A Block in a BlockChain. It contains the data to be stored and meta-data relevant to the Blockchain.
    -> Data: Data stored in the Block.
    -> Index: Position of the Block in the chain. Relevant as an identifier for the list only.
    -> Timestamp: Date and Time the Block was created
    -> Proof: A number which acts as the Nonce. This is relevant for mining the Block
    -> Previous Hash: Hash of the Block previous to the current in the BlockChain
    -> Hash: Hash of the Block. Hashing takes the data, timestamp, index and previous_hash as input
    """
    def __init__(self, proof, data, previous_hash):
        self.data = data
        self.previous_hash = previous_hash
        self.timestamp = str(datetime.now())
        self.proof = proof
        self.hash = ""
        self.index = 0

    def to_json(self):
        """
        A function to convert Block data and meta-data to a dictionary and return as a JSON string
        :return: A JSON string of the attributes af the Block
        """
        object_dictionary = {
            "data": self.data,
            "timestamp": self.timestamp,
            "index": self.index,
            "previous_hash": self.previous_hash
        }

        return json.dumps(object_dictionary, sort_keys= True)

    def hashed(self):
        """
        Function to hash the Block
        :return: void, sets the Block hash attribute internally
        """

        # Hash the JSON string of the Block
        encoded_block = self.to_json().encode()
        self.hash = hashlib.sha256(encoded_block).hexdigest()