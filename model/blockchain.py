import hashlib
from model.block import Block


class Blockchain:
    """
    The BlockChain class. Every instance of this class is a BlockChain. The object of this class consists of one attribute - Chain.
    When a new Object is created, a new chain is formed with the Genesis Block.
    """

    def __init__(self, data):
        self.chain = []

        # Creating the genesis block
        self.create_block(proof = 1, data= data, previous_hash = '0')

    def create_block(self, proof, data, previous_hash):
        """
        The create_block function instantiates the Block class, and adds the new Block to the Chain.
        :param proof: The nonce of the Block
        :param data: The data to be stored in the Block
        :param previous_hash: The hash of the previous Block in the Chain
        :return: The new created/mined Block
        """

        # Instantiate new block
        block = Block(proof, data, previous_hash)
        block.index = len(self.chain) + 1
        block.hashed()

        # Add block to the chain
        self.chain.append(block)
        return block

    def get_previous_block(self):
        """
        The last Block of the Chain is returned, It is required for mining.
        :return: The last Block in the BlockChain
        """
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        """
        The Proof Of Work (PoW) is the operation to find a new proof that fits the mining target
        and a new Block can be added to the Chain.

        Hash_operation -> The PoW operation to be performed between previous proof and new proof
        This tells us if the new proof is the golden Nonce and does it achieve mining Target.

        :param previous_proof: The proof of the previous Block in the BlockChain
        :return: The new proof value found to mine a new Block
        """

        new_proof = 1
        check_proof = False

        # Finding the right nonce for mining and defining the target
        while check_proof is False:
            # The operation between new and previous has to be asymmetrical
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()

            # Set a simple target so is doesn't take many iterations
            # If hash_operation starts with 4 zeros we have achieved target
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def is_chain_valid(self):
        """
        Checks whether the chain is valid or not.
        Two criteria for the validity
        -> Linkage: All Blocks in a BlockChain must be linked on the previous hash (Reverse linked List)
        -> Proof-Of-Work: The proofs of any two consecutive Blocks should satisfy the PoW (hash operation and target)
        :return: Boolean, whether chain is valid or not
        """

        previous_block = self.chain[0]
        block_index = 1

        # Loop on chain
        while block_index < len(self.chain):
            block = self.chain[block_index]

            # Check there is reverse linkage
            if block.previous_hash != previous_block.hash:
                return False

            previous_proof = previous_block.proof
            proof = block.proof

            # Check whether all hashes match our target of 4 leading zeros
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False

            previous_block = block
            block_index += 1

        return True