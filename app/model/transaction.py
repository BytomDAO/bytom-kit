import requests
import json

# submit_transaction broadcast raw transaction
# raw_transaction_str is signed transaction,
# network_str is mainnet or testnet
# test data 1:
#   raw_transaction_str: 070100010160015e0873eddd68c4ba07c9410984799928288ae771bdccc6d974e72c95727813461fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8094ebdc030101160014052620b86a6d5e07311d5019dffa3864ccc8a6bd630240312a052f36efb9826aa1021ec91bc6f125dd07f9c4bff87014612069527e15246518806b654d57fff8b6fe91866a19d5a2fb63a5894335fce92a7b4a7fcd340720e87ca3acdebdcad9a1d0f2caecf8ce0dbfc73d060807a210c6f225488347961402013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8082eee0020116001418028ef4f8b8c278907864a1977a5ee6707b2a6b00013cffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80b8b872011600142935e4869d0317d9701c80a02ecf888143cb9dd200
#   network_str: testnet
def submit_transaction(raw_transaction_str, network_str):
    raw_transaction_dict = {
        "transaction": raw_transaction_str
    }
    raw_transaction_json = json.dumps(raw_transaction_dict)
    headers = {
        "content-type": "application/json",
        "accept": "application/json"
    }
    if network_str == "mainnet":
        url = "https://blockmeta.com/api/v2/broadcast-transaction"
    else:
        url = "https://blockmeta.com/api/wisdom/broadcast-transaction"
    response = requests.post(url, headers=headers, data=raw_transaction_json)
    return {
        "response": response.text[:-1]
    }


def decode_raw_transaction(raw_transaction_str):
    raw_transaction_dict = {
        "raw_transaction": raw_transaction_str
    }
    raw_transaction_json = json.dumps(raw_transaction_dict)
    headers = {
        "content-type": "application/json",
        "accept": "application/json"
    }
    url = 'http://127.0.0.1:9888/decode-raw-transaction'
    response = requests.post(url, headers=headers, data=raw_transaction_json)
    return {
        "response": response.text[:-1]
    }
