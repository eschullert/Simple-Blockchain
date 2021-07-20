from blockchain import Blockchain
from wallet import Wallet
import random

# Wallets to do tests
w1 = Wallet('a','password')
w2 = Wallet('b','password')

# Path to key of w1 and w2
path2key1 = 'a_key.pem'
path2key2 = 'a_key.pem'

# Create new Blockchain
b = Blockchain()

# Add certain amount of money to wallets
for _ in range(random.randint(5,10)):
    wallet = random.choice([w1,w2])
    b.mine_pending_transaction(wallet)

q = False

while not q:
    paying_wallet = w1
    recieving_wallet = w2

    print("Balance a:",w1.balance)
    print("Balance b:",w2.balance)
    print('\n\nSelect action:')
    print('  anything -> a pays b.')
    print('   (r) reverse default.')
    print('   (q) quit')
    i = input('Selection: ')

    if i=='r':
        paying_wallet = w2
        recieving_wallet = w1

    if i=='q':
        print('Quitting...')
        q = True
    else:
        path = paying_wallet.username+'_key.pem'
        amount = float(input('Indicate amount to pay:'))
        b.add_transaction(paying_wallet,recieving_wallet,amount, 0, path, 'password')
        print('Payment made from',paying_wallet.username,'to',recieving_wallet.username,'of',amount)
        