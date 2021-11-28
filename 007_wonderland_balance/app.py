# 007_wonderland_balance/app.py
# enter wallet address into web app -> generate wonderland portfolio value

# dash app + morph theme DONE
# set up grid DONE
# enter wallet address and validate hex
# balances for TIME, MEMO, wMEMO, bonding rewards
# lookup market value of assets and calculate portfolio value

import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from dotenv import load_dotenv
import json
import os
from web3 import Web3

# import infura_url from .env or use your own
# infura_url = 'insert your url here'
load_dotenv()
INFURA_URL = os.getenv('INFURA_URL')
# create Infura connection
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Dash instance
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MORPH])

# Layout components
wallet_input = [
    dbc.Label(
        children='Enter Wallet Address',
        html_for='wallet_input',
        width=2,
    ),
    dbc.Col(
        children=dbc.Input(
            id='wallet_input',
            value='0xc2306a06993ebfb4a66b189c98fd1d5f03855349',
            type='text',
            autofocus=True,
        ),
        width=10
    )
]

time_balance = [
    dbc.Col(
        children='TIME balance',
        width=2
    ),
    dbc.Col(
        children='1.5',
        width=2
    ),
    dbc.Col(
        children='TIME price',
        width=2
    ),
    dbc.Col(
        children='$9000',
        width=2
    ),
    dbc.Col(
        children='TIME value',
        width=2
    ),
    dbc.Col(
        children='$13,500',
        width=2
    )
]

memo_balance = [
    dbc.Col(
        children='MEMO balance',
        width=2
    ),
    dbc.Col(
        children='1.5',
        width=2
    ),
    dbc.Col(
        children='MEMO price',
        width=2
    ),
    dbc.Col(
        children='$9000',
        width=2
    ),
    dbc.Col(
        children='MEMO value',
        width=2
    ),
    dbc.Col(
        children='$13,500',
        width=2
    )
]

wmemo_balance = [
    dbc.Col(
        children='wMEMO balance',
        width=2
    ),
    dbc.Col(
        children='1.5',
        width=2
    ),
    dbc.Col(
        children='wMEMO price',
        width=2
    ),
    dbc.Col(
        children='$9000',
        width=2
    ),
    dbc.Col(
        children='wMEMO value',
        width=2
    ),
    dbc.Col(
        children='$13,500',
        width=2
    )
]

# Layout
app.layout = dbc.Container([
    dbc.Row(
        children=dbc.Col(html.H1('Wonderland Portfolio Balance')),
        class_name='text-center mt-3'
    ),
    dbc.Row(
        children=wallet_input,
        class_name='my-4'
    ),
    dbc.Row(
        children=time_balance,
        class_name='text-center h4 my-3 p-3 bg-light rounded-3'
    ),
    dbc.Row(
        children=memo_balance,
        class_name='text-center h4 my-3 p-3 bg-light rounded-3'
    ),
    dbc.Row(
        children=wmemo_balance,
        class_name='text-center h4 my-3 p-3 bg-light rounded-3'
    ),
    html.Br(),
    html.Div(id='my-output'),
])

# Callback


def get_token_balance(wal_addr):
    ''' Get token balance in a wallet address

    Keyword arguments:
    wal_addr - wallet address
    '''
    ctrct_addr = '0x3845badAde8e6dFF049820680d1F14bD3903a5d0'
    checksum_address = web3.toChecksumAddress(ctrct_addr)
    wal_checksum = web3.toChecksumAddress(wal_addr)
    abi='[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newAdmin","type":"address"}],"name":"changeExecutionAdmin","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"amount","type":"uint256"}],"name":"approve","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"owner","type":"address"},{"name":"amount","type":"uint256"}],"name":"burnFor","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"from","type":"address"},{"name":"to","type":"address"},{"name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"owner","type":"address"},{"name":"spender","type":"address"},{"name":"amount","type":"uint256"}],"name":"approveFor","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"owner","type":"address"},{"name":"spender","type":"address"},{"name":"amountNeeded","type":"uint256"}],"name":"addAllowanceIfNeeded","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"burn","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"who","type":"address"}],"name":"isExecutionOperator","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"who","type":"address"}],"name":"isSuperOperator","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"executionOperator","type":"address"},{"name":"enabled","type":"bool"}],"name":"setExecutionOperator","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getAdmin","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"from","type":"address"},{"name":"to","type":"address"},{"name":"amount","type":"uint256"},{"name":"gasLimit","type":"uint256"},{"name":"data","type":"bytes"}],"name":"approveAndExecuteWithSpecificGas","outputs":[{"name":"success","type":"bool"},{"name":"returnData","type":"bytes"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newAdmin","type":"address"}],"name":"changeAdmin","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"superOperator","type":"address"},{"name":"enabled","type":"bool"}],"name":"setSuperOperator","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getExecutionAdmin","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"target","type":"address"},{"name":"amount","type":"uint256"},{"name":"data","type":"bytes"}],"name":"paidCall","outputs":[{"name":"","type":"bytes"}],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[{"name":"target","type":"address"},{"name":"amount","type":"uint256"},{"name":"data","type":"bytes"}],"name":"approveAndCall","outputs":[{"name":"","type":"bytes"}],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[{"name":"from","type":"address"},{"name":"to","type":"address"},{"name":"amount","type":"uint256"},{"name":"gasLimit","type":"uint256"},{"name":"tokenGasPrice","type":"uint256"},{"name":"baseGasCharge","type":"uint256"},{"name":"tokenReceiver","type":"address"},{"name":"data","type":"bytes"}],"name":"approveAndExecuteWithSpecificGasAndChargeForIt","outputs":[{"name":"success","type":"bool"},{"name":"returnData","type":"bytes"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"gasLimit","type":"uint256"},{"name":"data","type":"bytes"}],"name":"executeWithSpecificGas","outputs":[{"name":"success","type":"bool"},{"name":"returnData","type":"bytes"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"owner","type":"address"},{"name":"spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"from","type":"address"},{"name":"to","type":"address"},{"name":"amount","type":"uint256"},{"name":"gasLimit","type":"uint256"},{"name":"tokenGasPrice","type":"uint256"},{"name":"baseGasCharge","type":"uint256"},{"name":"tokenReceiver","type":"address"}],"name":"transferAndChargeForGas","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"sandAdmin","type":"address"},{"name":"executionAdmin","type":"address"},{"name":"beneficiary","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"superOperator","type":"address"},{"indexed":false,"name":"enabled","type":"bool"}],"name":"SuperOperator","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"oldAdmin","type":"address"},{"indexed":false,"name":"newAdmin","type":"address"}],"name":"AdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"oldAdmin","type":"address"},{"indexed":false,"name":"newAdmin","type":"address"}],"name":"ExecutionAdminAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"executionOperator","type":"address"},{"indexed":false,"name":"enabled","type":"bool"}],"name":"ExecutionOperator","type":"event"}]'
    abi = json.loads(abi)
    contract = web3.eth.contract(address=checksum_address, abi=abi)
    balance_wei = contract.functions.balanceOf(wal_checksum).call()
    balance = web3.fromWei(balance_wei, 'ether')
    return balance


@app.callback(
    Output(
        component_id='my-output',
        component_property='children'
        ),
    Input(
        component_id='wallet_input',
        component_property='value'
        ),
)
def update_output_div(input_value):
    balance = get_token_balance(wal_addr=input_value)
    return f'SAND balance: {balance}'


if __name__ == '__main__':
    app.run_server(debug=True)
