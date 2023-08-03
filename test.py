import requests
from pprint import pprint
from API_Keys.api_keys import datajockey



def test():
    ticker = "AAPL"
    query = f"https://api.datajockey.io/v0/company/financials/?ticker={ticker}&apikey={datajockey}"
    query = f"https://api.datajockey.io/v0/company/financials?ticker=AAPL&apikey={datajockey}"
    response = requests.get(query).json()

    pprint(f"Response: {response}")
test()