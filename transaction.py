'''
Single transaction in a block of the blockchain.

Classes:
    Transaction
'''
import struct
import utils

class Transaction:
    '''
    Single transaction in a block of the blockchain.

    Args:
        sending_wallet (Wallet): Wallet sending money.
        receiving_wallet (Wallet): Wallet recieving money.
        amount (float): amount of money transfered.
        fee (float): amount to pay to make the transaction.
        private_key (bytes): private key of the sending wallet.

    Attributes:
        sending_wallet (Wallet): Wallet sending money.
        receiving_wallet (Wallet): Wallet recieving money.
        amount (float): amount of money transfered.
        fee (float): amount to pay to make the transaction.
        signature (bytes): signature of the transaction using the private key.
    '''
    def __init__(
        self,
        sending_wallet: object,
        receiving_wallet: object,
        amount: float,
        fee: float,
        private_key: bytes
        ):
        self.sending_wallet = sending_wallet
        self.receiving_wallet = receiving_wallet
        self.amount = amount
        self.fee = fee
        if sending_wallet.username:
            self.signature = self.sign_transaction(private_key)

    def calculate_hash(self) -> bytes:
        '''
        Gets hash of the transaction.
        Hash is calculated with concatenation of:
        sending wallet hash + recieving wallet hash + amount.

        Returns:
            hash (bytes): hash of the transaction in bytes.
        '''
        return utils.sha256(
            self.sending_wallet.calculate_hash(),
            self.receiving_wallet.calculate_hash(),
            # binary structure calculated with little endian of two floats
            struct.pack('<ff', self.amount, self.fee)
            )

    def sign_transaction(self, private_key: object):
        '''
        Function used to sign a transaction using your private key.

        Args:
            private_key (object): private key needed to sign.

        Raises:
            Value Error
                Private key does not match sending wallet's public key.

        Returns:
            signature (bytes): signature of transaction using private key.
        '''
        # Private and public keys don't match
        if private_key.public_key() != self.sending_wallet.public_key:
            raise ValueError("Private key does not match the sending wallet's public key.")

        # Sign the transaction using the private key
        return private_key.sign(
            self.calculate_hash(),
            utils.ECDSA
            )

    def is_valid(self) -> bool:
        '''
        Checks if thetransactions is valid.
        Various conditions are required for a transaction being valid:
            1. Transaction requires sending, recieving and amount.
            2. Funds of sending wallet need to be suficient.
            3. Signature must match public key of sending wallet.

        Raises:
            ValueError:
                Transaction does not include sending, recieving or amount.
                Sending wallet funds insufficient.
                Signature and public key of sending wallet don't match.

        Return:
            is_valid (bool): boolean of if all transactions are valid.
        '''
        # Mining reward
        if not self.sending_wallet.username:
            return True

        if not self.sending_wallet or not self.receiving_wallet or not self.amount:
            raise ValueError('Transaction must include sending, recieving and amount')
        if self.amount + self.fee > self.sending_wallet.balance:
            raise ValueError('Sending wallet funds insufficient.')
        if self.sending_wallet.public_key.verify(self.signature, self.calculate_hash, utils.ECDSA):
            raise ValueError('Signature does not match public key of sending wallet.')
        return True
