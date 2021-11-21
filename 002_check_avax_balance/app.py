# app.py
# connect to Avax node and check balance of an address on C chain


from web3 import Web3


# create Avax connection
avalanche_url = 'https://api.avax.network/ext/bc/C/rpc'
web3 = Web3(Web3.HTTPProvider(avalanche_url))


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
    ''' Get balance of an avax address
    '''
    avax_address = '0xc255b73534DBd8C38a7a12a4e01Ad0061c376BBA'
    balance_wei = web3.eth.get_balance(avax_address)
    balance_eth = web3.fromWei(balance_wei, 'ether')
    print(f'Account balance is {balance_eth} AVAX.')


connect()
get_balance()
