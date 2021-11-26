# 006_pycoingecko_intro
# explore pycoingecko usage

import json
from pprint import pprint
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

# Check API server status
ping = cg.ping()
pprint(ping)

# Get coin price
coin_price = cg.get_price(ids='bitcoin', vs_currencies='usd')
pprint(coin_price)

# Save all supported coins to json
# coins_list = cg.get_coins_list()
# with open('coins_list.json', 'w') as file:
#     json.dump(coins_list, file)

# Save all supported coins market info to json
# coins_markets = cg.get_coins_markets(vs_currency='usd')
# with open('coins_markets.json', 'w') as file:
#     json.dump(coins_markets, file)

# 
