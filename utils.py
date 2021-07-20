'''
File with useful functions.

Functions:
    read_private_key(path: str, password: str) -> object
    merkle_root(hashList: list) -> str
    generate_key_pair(name: str, password: str) -> object

Misc Variables:
    ECDSA: Pre-hashed signature algorithm for  signing with private key
'''
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import utils

ECDSA = ec.ECDSA(utils.Prehashed(hashes.SHA256()))
PEM_ENCODING = serialization.Encoding.PEM
DER_ENCODING = serialization.Encoding.DER
PRIVATE_KEY_FORMAT = serialization.PrivateFormat.PKCS8
PUBLIC_KEY_FORMAT = serialization.PublicFormat.SubjectPublicKeyInfo

def read_private_key(path: str, password: str) -> object:
    '''
    Reads the private key PEM file and returns a private key.

    Args:
        password (str): password for the PEM file of the private key.

    Returns:
        private_key (object): private key in the file.
    '''
    with open(path,'rt') as f:
        data = bytes(f.read(), 'utf-8')
    return load_pem_private_key(data, bytes(password, 'utf-8'))

def merkle_root(hashList: list) -> bytes:
    '''
    Function to calculate the Merkle Root of a list of hashes.
    Recursive function traverses the levels of a Merkle Tree until
    it reaches a the Merkle Root.

    It works by hashing the concatenation of pairs of hashes (if number
    of hashes is odd the last one is concatenated with itself) until
    it has only one hash left, the Merkle Root.
    See https://en.wikipedia.org/wiki/Merkle_tree.
    Based in code from Ken Shirriff's blog.

    Args:
        hashList (list): List of strings of hashes.

    Returns:
        newList (list): List of hashes(while recursive).
        merkle_root (str): hash of the merkle root in bytes.
    '''
    if not hashList: # if it is empy return hash of empty
        return sha256(b'')

    if len(hashList) == 1: # If only one value it is the merkle root
        return hashList[0]

    # List of concatenated pairs of hashes
    pairList = [(a,b) for a,b in zip(hashList[::2],hashList[1::2])]

    # if len(hashList) is odd then last pair is last item twice
    if len(hashList) % 2 == 1: #
        pairList.append((hashList[-1],hashList[-1]))

    # do all the hashes
    # Input and output is reversed in each case because
    # little endian / big endian
    newHashes = [sha256(a[::-1],b[::-1])[::-1] for a,b in pairList]
    return merkle_root(newHashes)

def generate_key_pair(name: str, password: str, save_private: bool = True):
    '''
    Generates a pair of public and private keys using Elliptic Curves.
    Uses a SEC256R1 curve for the encryption.

    Saves the private key as a pem file. It doesn't saves the private
    key anywhere else so it is important to not delete it.
    PRIVATE KEY CANNOT BE REPLACED, SAVE IT.

    Args:
        name (str): name passed to save the PEM file of the private key.
        password (str): password for the encryption of the private key PEM.
        save_private (bool = True):  Decides if it saves the private key in computer

    Returns:
        public_key (object): Public key associated with the private key in PEM file.
    '''
    private_key = ec.generate_private_key(ec.SECP256R1())

    if save_private:
        # Converting the private key to text to save it in file
        private_key_txt = private_key.private_bytes(
            encoding = PEM_ENCODING,
            format = PRIVATE_KEY_FORMAT,
            encryption_algorithm = serialization.BestAvailableEncryption(bytes(password,'utf-8'))
            ).decode('utf-8')

        with open(name+'_key.pem','wt') as f:
            f.write(private_key_txt)

    return private_key.public_key()

def sha256(*args: bytes):
    '''
    Hash n arguments using SHA256. REquires at least 1 argument.

    Args:
        *args (bytes): things to hash.

    Raises:
        TypeError
            There are no arguments to hash.

    Returns:
        hash (bytes): hash of arguments.
    '''
    if not args:
        raise TypeError('At least 1 argument is required.')
    digest = hashes.Hash(hashes.SHA256())
    for arg in args:
        digest.update(arg)
    return digest.finalize()
