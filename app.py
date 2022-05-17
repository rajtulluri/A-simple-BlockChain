import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import json
from flask import Flask, jsonify, request
from model.blockchain import Blockchain

app: Flask = Flask(__name__)
app.config.from_pyfile("config.py")

# Instantiate a new BlockChain, The chain consists of only Genesis Block
blockchain = Blockchain("Genesis block")


@app.route('/mine_block', methods=['POST'])
def mine_block():
    """
    POST API to mine a new Block. It performs:
     -> PoW to get golden Nonce
     -> Creates new Block with posted data
    :return: JSON, response acknowledging mining of new Block
    """
    # Extract JSON request from POST
    content = request.json

    # obtain previous proof for PoW calculations
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block.proof
    proof = blockchain.proof_of_work(previous_proof)

    # Create new mined block
    block = blockchain.create_block(proof, content['data'], previous_block.hash)

    # Build Response packet
    response = {
        "message": 'Congrats, you have mined a block',
        "index": block.index,
        "timestamp": block.timestamp,
        "proof": block.proof,
        "previous_hash": block.previous_hash
    }

    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    """
    View the current BlockChain list. This function is only for the purpose of this example
    The BlockChain in reality shouldn't be public.
    :return: BlockChain as a list of JSONs
    """

    response = {
        'chain': [json.loads(block.to_json()) for block in blockchain.chain],
        'length': len(blockchain.chain)
    }

    return jsonify(response), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    """
    Check the validity of the BlockChain. This function helps us to observe if the BlockChain has been
    compromised at any point.
    :return: JSON response, with Boolean status
    """

    # Check validity via reverse linkage and PoW
    validity = blockchain.is_chain_valid()

    response = {
        "Success": validity,
        "message": "The blockchain is valid" if validity else "The blockchain is not valid"
    }

    return jsonify(response), 200


app.run(debug=True)
