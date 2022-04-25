import hashlib
import json
from time import time
from zkp import verify

import pickle
import os

class Blockchain(object):

    chain_list = []

    def __init__(self, user):
        self.chain = []
        self.current_transactions = []
        self.user = user

        # Create the genesis Block
        self.new_block(previous_hash=1, nounce=100)

        # Load the Blockchain 
        Blockchain.load_blockchains()
        
    def new_block(self, nounce, previous_hash=None):
        """
        Forge a new Block in the Blockchain
        :param nouce is used to satisfy the difficulty for the Proof of Work algorithm
        :return return the new Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'nounce': nounce,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        print("block created: {}".format(block))

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        Blockchain.save_blockchains()
        return block
    
    def new_transaction(self, user, doctor, visit_type, report, medicine, tuple):
        # Adding transaction to the list of transactions to be mined

        if (not verify(tuple)):
            return False

        self.current_transactions.append({
            'user': user,
            'doctor': doctor,
            'visit_type': visit_type,
            'report': report,
            'medicine': medicine,
        })

        return self.last_block['index'] + 1
    
    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        """

        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_nounce):
        """
        PoW Algorithm:
        - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
        - p is the previous nounce, and p' is the new nounce
        :param last_nounce: <int>
        :return: <int>
        """

        nounce = 0
        while self.valid_proof(last_nounce, nounce) is False:
            nounce += 1

        return nounce

    @staticmethod
    def valid_proof(last_nounce, nounce):
        """
        Check if a nounce is valid
        :return: <bool> True if correct, False if not
        """

        guess = f'{last_nounce}{nounce}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        if (guess_hash[:4] == "0000"):
            print("Validated: p = {}, p' = {}".format(last_nounce, nounce))
            return True
        return False

    @staticmethod
    def create_new_blockchain(user):

        """
        Create a new Blockchain
        """

        new_blockchain = Blockchain(user)
        Blockchain.chain_list.append(new_blockchain)
        Blockchain.save_blockchains()

        return new_blockchain

    @staticmethod
    def save_blockchains():
        """
        Save the current Blockchains to the database file
        """

        if not os.path.isfile('database'):
            open('database', 'x')  

        with open('database', 'wb') as file:
            pickle.dump(Blockchain.chain_list, file)

    @staticmethod
    def load_blockchains():
        """
        Load the Blockchains from the database file
        """
        Blockchain.chain_list = []

        if not os.path.isfile('database'):
            open('database', 'x')  

        if os.stat('database').st_size > 0:
            with open('database', 'rb') as file:
                Blockchain.chain_list = pickle.load(file)

        print(Blockchain.chain_list)

    def mine(user):

        blockchain = Blockchain.get_blockchain(user)

        last_block = blockchain.last_block
        last_nounce = last_block['nounce']
        nounce = blockchain.proof_of_work(last_nounce)

        # No reward for mining :P 

        # Forge the new Block by adding it to the chain
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(nounce, previous_hash)

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'nounce': block['nounce'],
            'previous_hash': block['previous_hash'],
        }
        return response

    
    def create_transaction(user, doctor, visit_type, report, medicine, tuple):

        blockchain = Blockchain.get_blockchain(doctor)

        # Create a new Transaction
        index = blockchain.new_transaction(user, doctor, visit_type, report, medicine, tuple)

        response = {'message': f'Transaction will be added to Block {index}'}
        return response

    
    @staticmethod
    def get_blockchain(user):

        for blockchain in Blockchain.chain_list:
            if blockchain.user == user:
                return blockchain

        return Blockchain.create_new_blockchain(user)
            
    @staticmethod
    def search_blockchain(user):

        for blockchain in Blockchain.chain_list:
            if blockchain.user == user:
                return blockchain

        return None