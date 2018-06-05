import hashlib
import json
#from textwrap import dedent
from time import time
from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask, jsonify, request
import requests

class Blockchain:
    def __init__(self):##Check
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        #Genesis Block
        self.new_block(previous_hash='1', proof=100)



    def new_block(self,proof,previous_hash=None):##diff
        '''
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        '''
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        #Resets current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block




    def new_transaction(self, sender, recipient, amount):##Check
        '''
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        '''
        self.current_transactions.append({'sender':sender, 'recipient':recipient, 'amount':amount,})
        return self.last_block["index"]+1
        


    def register_node(self, address):##Check
        '''
        Add a new node to the list of nodes
        :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        :return: None
        '''
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)




    def valid_chain(self, chain):##Check
        '''
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        '''
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print (f'{last_block}')
            print (f'{block}')
            print ("\n-----------\n")
            #Check that hash of block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            #Check that proof of work is correct
            if not self.valid_proof(last_block['proof'], block['proof'],last_block_hash):
                return False
            last_block = block
            current_index += 1
            return True


    def resolve_conflicts(self):##Check
        '''
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        '''
        neighbours = self.nodes
        new_chain = None

        #We're only lookin for chains longer than ours
        max_length = len(self.chain)

        #Grab and verify chains from all nodes in network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                #Check if length is longer and chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        #Replace our chain if we discovered a new, valid chain longer
        if new_chain:
            self.chain = new_chain
            return True
        return False


    @staticmethod
    def hash(block):##Check
        '''
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        '''

        #Make sure dictionary is ordered, or it'll result in inconsistent hashes
        block_string = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):##Check
        return self.chain[-1]

    def proof_of_work(self, last_proof):##Diff
        '''
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        '''
        
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof,proof):##Check
        '''
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        '''
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"




#########################

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()



@app.route('/mine', methods=['GET'])
def mine():
    #Run the prrof of work algorithm to get next proof
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    #Must receive a reward for finding the proof
    #The send is "0" to signify creation of new coin
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
        )

    #Forge new block by adding to chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof,previous_hash)

    response= {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        }
    return jsonify(response),200

@app.route('/transactions/new', methods=['POST'])##Check
def new_transaction():
    values = request.get_json()
    #Check out required fields are int POSTed data
    required = ['sender','recipient','amount']
    if not all(k in values for k in required):
        return 'Missing values',400
    #Create new transaction
    index = blockchain.new_transaction(values['sender'],values['recipient'],values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response),201



@app.route('/chain', methods=['GET'])##Check
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200



@app.route('/nodes/register',methods=['POST'])##Check
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes",400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response),201


@app.route('/nodes/resolve',methods=['GET'])##Check
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
    return jsonify(response),200

if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=5000)
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    #app.run(host='0.0.0.0', port=5001)

    app.run(host='0.0.0.0', port=port)
    app.run(host='0.0.0.0', port=5001)











