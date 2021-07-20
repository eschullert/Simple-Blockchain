'''
Wallet that can make transactions in the blockchain.

Classes:
    Wallet
'''
import utils

class Wallet:
    '''
    Single coin wallet in the Blockchain.

    Args:
        username (str): username of the wallet.
        password (str): password to make transactions.

    Attributes:
        username (str): username of the wallet.
        public_key (bytes): public key used in the encryption.
    '''
    def __init__(self, username: str, password: str):
        if not username:
            self.username = ''
            self.public_key = utils.generate_key_pair('','', False)
        elif not username.isalnum(): # username has to be alphanumeric
            raise ValueError('Username must only contain alphanumeric values.')
        else:
            self.username = username
            self.public_key = utils.generate_key_pair(username, password)
            self.balance = 0

    def calculate_hash(self):
        '''
        Gets hash of the wallet.
        Hash is calculated with concatenation of:
        username+ public key.

        Returns:
            hash (bytes): hash of the transaction in bytes.
        '''
        return utils.sha256(
            bytes(self.username, 'utf-8'),
            self.public_key.public_bytes(
                utils.DER_ENCODING,
                utils.PUBLIC_KEY_FORMAT
                )
            )
