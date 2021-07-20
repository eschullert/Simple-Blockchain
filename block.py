'''
Single block of a Blockchain.

Classes:
    Block
'''
import struct
from time import time
import utils

class Block:
    '''
    Single Block in a Blockchain.

    Args:
        prev_hash (str): hash of previous block in HEX.
        transactions (list): list of transactions in the block.

    Attributes:
        prev_hash (bytes): hash of previous block.
        transactions (list): list of transactions in the block.
        timestamp (int): Unix timestamp.
        merkle_root (bytes): HEX hash of merkle root of transactions.
        nonce (int): number incremented to change the hash for mining.
        hash (bytes): final hash of the block.
    '''
    def __init__(self, prev_hash: bytes, transactions: list):
        self.previous_hash = prev_hash
        self.transactions = transactions
        self.timestamp = time()
        self.merkle_root = utils.merkle_root(
            [trans.calculate_hash() for trans in self.transactions]
            )
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> bytes:
        '''
        Gets hash of the Block.
        Hash is calculated with concatenation of:
        previous hash + merkle root of transaction + timestamp.

        Returns:
            hash (bytes): hash of the block in bytes.
        '''
        return utils.sha256(
            self.previous_hash[::-1],
            self.merkle_root[::-1],
            struct.pack( # binary structure
                '<fi',   #using little endian, float, int
                self.timestamp,
                self.nonce
                )
            )

    def has_valid_transactions(self) -> bool:
        '''
        Checks if all the transactions in the block are valid.
        Transaction validity checked in the Transaction class
        on transaction.py document.

        Return:
            is_valid (bool): boolean of if all transactions are valid.
        '''
        return all((tx.is_valid() for tx in self.transactions))

    def mine(self, difficulty):
        while any((i!=0 for i in self.calculate_hash()[:difficulty])):
            self.nonce += 1

        self.hash = self.calculate_hash()

        for transaction in self.transactions:
            if transaction.sending_wallet.username: #if it is not a mining reward
                transaction.sending_wallet.balance -= (transaction.amount + transaction.fee)
            transaction.receiving_wallet.balance += transaction.amount
