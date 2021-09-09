import sys
import hashlib
import json
import requests
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
from urllib.parse import urlparse

class Blockchain(object):
    difficulty_target = "0000"

    def hash_block(self, block):
        block_encoded = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_encoded).hexdigest()

    def __init__(self):
        self.chain = []
        self.current_transactions = []

        genesis_hash = self.hash_block("genesis_block")

        self.append_block(hash_of_previous_block = genesis_hash, nonce = self.proof_of_work(0, genesis_hash, []))

    # use PoW to find the nonce for the current block
    def proof_of_work(self, index, hash_of_previous_block, transactions):
        # try with nonce = 0
        nonce = 0

        #try hashing the nonce together with the hash of the preivous block untils is valid
        while self.valid_proof(index, hash_of_previous_block, transactions, nonce) is False:
            nonce += 1

        return nonce

    # hashes the content of a block and check to see if the block's hash meets the difficulty target
    def valid_proof(self, index, hash_of_previous_block, transactions, nonce):

        # create a stirng containing the hash of the previous block and the block content, including the nonce

        content = f'{index}{hash_of_previous_block}{transactions}{nonce}'.encode()

        # hash using sha256
        content_hash = hashlib.sha256(content).hexdigest()

        # check if the hash meets the difficulty target
        return content_hash[:len(self.difficulty_target)] == self.difficulty_target

