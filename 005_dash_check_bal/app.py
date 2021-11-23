# 005_dash_check_bal/app.py
# use Dash to check SAND balance in a wallet address

import dash
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html
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
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H3("Enter a wallet address to see the SAND balance"),
    html.Div([
        "Wallet Address: ",
        dcc.Input(
            id='my-input',
            value='0xc2306a06993ebfb4a66b189c98fd1d5f03855349',
            type='text')
    ]),
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
        component_id='my-input',
        component_property='value'
        ),
)
def update_output_div(input_value):
    balance = get_token_balance(wal_addr=input_value)
    return f'SAND balance: {balance}'


if __name__ == '__main__':
    app.run_server(debug=True)
