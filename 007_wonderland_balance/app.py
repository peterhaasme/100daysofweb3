# 007_wonderland_balance/app.py
# enter wallet address into web app -> generate wonderland portfolio value

# dash app + morph theme DONE
# set up grid DONE
# enter wallet address and validate hex DONE
# balances for TIME, MEMO, wMEMO DONE
# bonding rewards
# lookup market value of assets and calculate portfolio value

import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from dotenv import load_dotenv
import json
import os
import requests
from token_info import tokens
from web3 import Web3

# INSTANCES ###

# Dash instance
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MORPH])

# import nomics API key from .env
load_dotenv()
NOMICS_API_KEY = os.getenv('NOMICS_API_KEY')

# create Avax connection
avalanche_url = 'https://api.avax.network/ext/bc/C/rpc'
web3 = Web3(Web3.HTTPProvider(avalanche_url))

# LAYOUT ###
# Layout components
wallet_input = [
    dbc.Label(
        children=html.H5('Enter Wallet Address'),
        html_for='wallet_input',
        width=2,
    ),
    dbc.Col(
        children=[
            dbc.Input(
                id='wallet_input',
                value='0x104d5ebb38af1ae5eb469b86922d1f10808eb35f',
                type='text',
                autofocus=True
            ),
            dbc.FormFeedback(
                children="Valid address",
                type="valid"
            ),
            dbc.FormFeedback(
                children="Invalid address",
                type="invalid",
            ),
        ],
        width=10
    )
]

time_balance = [
    dbc.Col(
        children='TIME balance',
        width=6,
        lg=2
    ),
    dbc.Col(
        id='time_balance',
        children='',
        width=6,
        lg=2
    ),
    dbc.Col(
        children='TIME price',
        width=6,
        lg=2
    ),
    dbc.Col(
        id='time_price',
        children='',
        width=6,
        lg=2
    ),
    dbc.Col(
        children='TIME value',
        width=6,
        lg=2
    ),
    dbc.Col(
        id='time_value',
        children='',
        width=6,
        lg=2
    )
]

memo_balance = [
    dbc.Col(
        children='MEMO balance',
        width=6,
        lg=2
    ),
    dbc.Col(
        id='memo_balance',
        children='',
        width=6,
        lg=2
    ),
    dbc.Col(
        children='MEMO price',
        width=6,
        lg=2
    ),
    dbc.Col(
        id='memo_price',
        children='',
        width=6,
        lg=2
    ),
    dbc.Col(
        children='MEMO value',
        width=6,
        lg=2
    ),
    dbc.Col(
        id='memo_value',
        children='',
        width=6,
        lg=2
    )
]

wmemo_balance = [
    dbc.Col(
        children='wMEMO balance',
        width=6,
        lg=2
    ),
    dbc.Col(
        id='wmemo_balance',
        children='',
        width=6,
        lg=2
    ),
    dbc.Col(
        children='wMEMO price',
        width=6,
        lg=2
    ),
    dbc.Col(
        id='wmemo_price',
        children='',
        width=6,
        lg=2
    ),
    dbc.Col(
        children='wMEMO value',
        width=6,
        lg=2
    ),
    dbc.Col(
        id='wmemo_value',
        children='',
        width=6,
        lg=2
    )
]

total_value = [
    dbc.Col(
        id='total_value',
        children=''
    )
]

interval = dcc.Interval(
            id='price_interval',
            interval=60000,  # 60000ms=1min
            n_intervals=0
        )

credits = dbc.Col(
    dcc.Markdown('''
        ##### Credits
        Price Data - [Nomics](https://p.nomics.com/cryptocurrency-bitcoin-api)
    ''')
)

notes = dbc.Col(
    dcc.Markdown('''
        ##### Notes
        - Refresh every 60s
        - Test addresses:
            - TIME -> 0x104d5ebb38af1ae5eb469b86922d1f10808eb35f
            - MEMO -> 0xe7ca3ff841ee183e69a38671927290a34de49567
            - wMEMO -> 0xdcf6f52faf50d9e0b6df301003b90979d232400e
        - Coming soon: bonding rewards balance
    ''')
)

# Page Layout
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
    dbc.Row(
        children=total_value,
        class_name='text-center text-light h3 my-3 p-3 bg-info rounded-3'
    ),
    dbc.Row(
        children=credits,
        class_name=''
    ),
    dbc.Row(
        children=notes,
        class_name=''
    ),
    interval,
    html.Br(),
    html.Div(id='my-output'),
])

# CALLBACKS ###


@app.callback(
    Output(
        component_id="wallet_input",
        component_property="valid"
    ),
    Output(
        component_id="wallet_input",
        component_property="invalid"
    ),
    Input(
        component_id="wallet_input",
        component_property="value"
    ),
)
def check_validity(value):
    ''' Validate wallet address
    '''
    if value:
        return Web3.isAddress(value), not Web3.isAddress(value)
    return False, False


def get_token_balance(token, wal_addr, currency):
    ''' Get token balance in a wallet address

    Keyword arguments:
    token - token symbol
    wal_addr - wallet address
    currency - denomination https://web3py.readthedocs.io/en/stable/examples.html?#converting-currency-denominations
    '''
    ctrct_addr = tokens[token]['address']
    checksum_address = web3.toChecksumAddress(ctrct_addr)
    wal_checksum = web3.toChecksumAddress(wal_addr)
    abi = tokens['time']['abi']
    abi = json.loads(abi)
    contract = web3.eth.contract(address=checksum_address, abi=abi)
    balance_gwei = contract.functions.balanceOf(wal_checksum).call()
    balance = web3.fromWei(balance_gwei, currency)
    return balance


@app.callback(
    Output(
        component_id='time_balance',
        component_property='children'
    ),
    Output(
        component_id='memo_balance',
        component_property='children'
    ),
    Output(
        component_id='wmemo_balance',
        component_property='children'
    ),
    Output(
        component_id='time_price',
        component_property='children'
    ),
    Output(
        component_id='memo_price',
        component_property='children'
    ),
    Output(
        component_id='wmemo_price',
        component_property='children'
    ),
    Output(
        component_id='time_value',
        component_property='children'
    ),
    Output(
        component_id='memo_value',
        component_property='children'
    ),
    Output(
        component_id='wmemo_value',
        component_property='children'
    ),
    Output(
        component_id='total_value',
        component_property='children'
    ),
    Input(
        component_id='wallet_input',
        component_property='valid'
    ),
    Input(
        component_id='wallet_input',
        component_property='value'
    ),
    Input(
        component_id='price_interval',
        component_property='n_intervals'
    ),
)
def display_balances(valid, value, n):
    ''' Get token balances and prices. Compute indiv and total value.
    '''
    # If the wallet address is valid retrieve balances
    if valid:
        time_bal = get_token_balance(
            token='time',
            wal_addr=value,
            currency='gwei'
        )
        memo_bal = get_token_balance(
            token='memo',
            wal_addr=value,
            currency='gwei'
        )
        wmemo_bal = get_token_balance(
            token='wmemo',
            wal_addr=value,
            currency='ether'
        )
        time_bal_show = round(time_bal, 2)
        memo_bal_show = round(memo_bal, 2)
        wmemo_bal_show = round(wmemo_bal, 5)
    else:
        time_bal_show = '0'
        memo_bal_show = '0'
        wmemo_bal_show = '0'

    # Get token prices. MEMO = TIME
    url = 'https://api.nomics.com/v1/currencies/ticker'
    payload = {
        'key': NOMICS_API_KEY,
        'ids': 'TIME5,WMEMO'
    }
    response = requests.get(url, params=payload)
    time_price = response.json()[0]['price']
    time_price_show = f'${float(time_price):,.2f}'
    wmemo_price = response.json()[1]['price']
    wmemo_price_show = f'${float(wmemo_price):,.2f}'

    # If the wallet address is valid compute values
    if valid:
        time_value = float(time_bal) * float(time_price)
        time_value_show = f'${time_value:,.2f}'
        memo_value = float(memo_bal) * float(time_price)
        memo_value_show = f'${memo_value:,.2f}'
        wmemo_value = float(wmemo_bal) * float(wmemo_price)
        wmemo_value_show = f'${wmemo_value:,.2f}'
    else:
        time_value_show = '$0'
        memo_value_show = '$0'
        wmemo_value_show = '$0'

    # Calculate total value
    total_value = time_value + memo_value + wmemo_value
    total_value_show = f'Total Value = ${total_value:,.2f}'

    # Return values
    return (time_bal_show, memo_bal_show, wmemo_bal_show, time_price_show,
            time_price_show, wmemo_price_show, time_value_show, memo_value_show,
            wmemo_value_show, total_value_show)


if __name__ == '__main__':
    app.run_server(debug=True)
