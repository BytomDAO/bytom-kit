import requests
import json

# broadcast_transaction broadcast raw transaction
# raw_transaction_str is signed transaction,
# network_str is mainnet or testnet
def broadcast_transaction(raw_transaction_str, network_str):
    raw_transaction_dict = {
        "transaction": raw_transaction_str
    }
    raw_transaction_json = json.dumps(raw_transaction_dict)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    if network_str == "mainnet":
        url = "https://blockmeta.com/api/v2/broadcast-transaction"
    else:
        url = "https://blockmeta.com/api/wisdom/broadcast-transaction"
    response = requests.post(url, headers=headers, data=raw_transaction_json)
    return response



