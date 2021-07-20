'''
Simple Blockchain class.

Classes:
    Blockchain
'''
from block import Block
from transaction import Transaction
from wallet import Wallet
import utils

class Blockchain:
    '''
    Complete Blockchain.

    Attributes:
        chain (list): list of Blocks that make the Blockchain.
        difficulty (int): number of zeroes at beginning of hashes to calculate.
        pending_transactions (list): transactions that are not yet in the chain.
        mining_reward (float): number of coins rewarded for mining a block.
        mining_block (Block): Block that it is currently being mined
            # TODO: Concurrency will be added here using this attribute
    '''
    def __init__(self):
        self.chain = [Block(b'',[])]
        self.difficulty = 1
        self.pending_transactions = []
        self.mining_reward = 50.0
        self.mining_block = None
        self.reward_wallet = Wallet('','')

    def add_transaction(
        self,
        send_wallet: Wallet,
        recieve_wallet: Wallet,
        amount: float,
        fee: float,
        path: str,
        password: str
        ):
        '''
        Validates a transaction and adds it to the pending transactions.

        Args:
            send_wallet (Wallet): wallet sending money.
            recieve_wallet (Wallet): wallet receiving money.
            amount (float): amount of money sent.
            fee (float): fee paid.
            path (str): path to private key of sending wallet.
            password (str): password of private key.
                # TODO: Last two temporary to do tests more quickly
        '''
        pk = utils.read_private_key(path, password)
        transaction = Transaction(send_wallet, recieve_wallet, amount,  fee, pk)
        if transaction.is_valid():
            self.pending_transactions.append(transaction)

    def halving(self):
        '''
        Halves reward for mining.
        '''
        self.mining_reward /= 2

    def new_block(self):
        '''
        Create a new block to start mining it.
        '''
        self.mining_block  = Block(
            self.chain[-1].hash,
            self.pending_transactions
            )


    def mine_pending_transaction(self, wallet: Wallet):
        '''
        Mine new block to place pending transactions.

        Args:
            wallet (Wallet): Wallet that mined the coin
        '''
        # Create a new block at the end of the chain
        if not self.mining_block:
            self.new_block()

        # Block is mineed and added to chain
        self.mining_block.mine(self.difficulty)
        self.chain.append(self.mining_block)

        # First transaction of next block is the reward for mining.
        self.pending_transactions = [Transaction(
            self.reward_wallet,
            wallet,
            self.mining_reward,
            0,
            None
        )]

        # Empty attribute so transactions can be generated again before mining again.
        # This is temporal. In the future it will be async and rewarding wallet pools.
        self.mining_block = None

        #Increase difficulty with number of blocks
        if len(self.chain) % 10 == 0:
            self.difficulty += 1

    def verify_balance(self, wallet: Wallet) -> bool:
        '''
        Verify the balance of a wallet.

        Args:
            wallet (Wallet): wallet to verify the balance.

        Returns:
            is_valid (bool): boolean if balance is valid according to transactions.
        '''
        balance = 0
        for block in self.chain:
            for t in block.transactions:
                if t.sending_wallet == wallet:
                    balance -= (t.amount+t.fee)
                if t.receiving_wallet == wallet:
                    balance += t.amount
        return balance == wallet.balance

    def verify_blockchain(self):
        '''
        Verifies the hashes of the blockchain to see if they are correct.
        '''
        return all((block.hash == block.calculate_hash() for block in self.chain))
