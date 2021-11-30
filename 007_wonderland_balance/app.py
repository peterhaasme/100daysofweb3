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

from decimal import Decimal
import json
from pycoingecko import CoinGeckoAPI
from token_info import tokens
from web3 import Web3

# Dash instance
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MORPH])

# Coingecko API instance
cg = CoinGeckoAPI()

# create Avax connection
avalanche_url = 'https://api.avax.network/ext/bc/C/rpc'
web3 = Web3(Web3.HTTPProvider(avalanche_url))

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
        id='memo_price',
        children='',
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

total_value = [
    dbc.Col(
        children='Total Value = $10,000'
    )
]

interval = dcc.Interval(
            id='price_interval',
            interval=60000, # 60000ms=1min
            n_intervals=0
        )

credits = dbc.Col(
    dcc.Markdown('''
        ##### Credits
        Price Data - [Coingecko](https://www.coingecko.com/en/api)
    ''')
)

notes = dbc.Col(
    dcc.Markdown('''
        ##### Notes
        - Refresh every 60s
    ''')
)

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

# Callback


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


def get_token_balance(token, wal_addr):
    ''' Get token balance in a wallet address

    Keyword arguments:
    token - token symbol
    wal_addr - wallet address
    '''
    ctrct_addr = tokens[token]['address']
    checksum_address = web3.toChecksumAddress(ctrct_addr)
    wal_checksum = web3.toChecksumAddress(wal_addr)
    abi = tokens['time']['abi']
    abi = json.loads(abi)
    contract = web3.eth.contract(address=checksum_address, abi=abi)
    balance_gwei = contract.functions.balanceOf(wal_checksum).call()
    balance = web3.fromWei(balance_gwei, 'gwei')
    return balance


@app.callback(
    Output(
        component_id='time_balance',
        component_property='children'
    ),
    Output(
        component_id='time_price',
        component_property='children'
    ),
    Output(
        component_id='time_value',
        component_property='children'
    ),
    Input(
        component_id='price_interval',
        component_property='n_intervals'
    ),
    Input(
        component_id='wallet_input',
        component_property='valid'
    ),
    Input(
        component_id='wallet_input',
        component_property='value'
    ),
)
def time_value(n, valid, value):
    ''' If the wallet address is valid populate TIME balance, price, value
    '''
    if valid:
        time_price = cg.get_price(
            ids='wonderland',
            vs_currencies='usd'
        )
        time_price_2 = time_price['wonderland']['usd'] # type float
        time_price_3 = "${:,.2f}".format(time_price_2)
        balance = round(get_token_balance(token='time', wal_addr=value), 2)
        time_value = "${:,.2f}".format(time_price_2*float(balance))
    else:
        time_price_3 = '$0'
        balance = '0'
        time_value = '$0'
    return balance, time_price_3, time_value

if __name__ == '__main__':
    app.run_server(debug=True)
