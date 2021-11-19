from dotenv import load_dotenv
import os
from web3 import Web3

# import infura_url from .env or use your own
# infura_url = 'insert your url here'
load_dotenv()
INFURA_URL = os.getenv('INFURA_URL')

# create Infura connection
web3 = Web3(Web3.HTTPProvider(INFURA_URL))


def connect():
    ''' Verify connection and show latest block number
    '''
    # Connect to remote node
    is_connected = web3.isConnected()
    latest_block = web3.eth.blockNumber
    if is_connected:
        print(f'Connection Made. Latest block is {latest_block}.')
    else:
        print('Connection Failed')


def get_balance():
    ''' Get balance of an ethereum address
    '''
    eth_address = '0x88DF69632184b387B1C185393a832b92AB462B31'
    balance_wei = web3.eth.get_balance(eth_address)
    balance_eth = web3.fromWei(balance_wei, 'ether')
    print(f'Account balance is {balance_eth} ETH.')


connect()
get_balance()
