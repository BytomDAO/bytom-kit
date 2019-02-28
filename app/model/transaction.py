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


def get_uvarint(uvarint_str):
    uvarint_bytes = bytes.fromhex(uvarint_str)
    x, s, i = 0, 0, 0
    while True:
        b = uvarint_bytes[i]
        if b < 0x80:
            if i > 9 or i == 9 and b > 1:
                return "overflow"
            return x | int(b) << s, i + 1
        x |= int(b & 0x7f) << s
        s += 7
        i += 1


# def decode_raw_tx(raw_tx_str):
#     tx_input = {
#         "address": "",
#         "amount": 0,
#         "asset_definition": {},
#         "asset_id": "",
#         "control_program": "",
#         "input_id": "",
#         "spend_output_id": "",
#         "type": "",
#         "witness_arguments": []
#     }
#     tx_output = {
#         "address": "",
#         "amount": 0,
#         "asset_definition": {},
#         "asset_id": "",
#         "control_program": "",
#         "id": "",
#         "position": 0,
#         "type": ""
#     }
#     tx = {
#         "fee": 0,
#         "inputs": [],
#         "outputs": [],
#         "size": 0,
#         "time_range": 0,
#         "tx_id": "",
#         "version": 0
#     }
#     version = int(raw_tx_str[2:4], 16)
#     time_range = int(raw_tx_str[4:6], 16)
#     tx_input_amount = int(raw_tx_str[6:8], 16)
#     tx_input_version = int(raw_tx_str[8:10], 16)
#     tx_input_length = int(raw_tx_str[10:12], 16)
#     tx_input_type = int(raw_tx_str[12:14], 16)
#     tx_input_data_spend_commit_length = int(raw_tx_str[14:16], 16)
#     tx_input_source_id = raw_tx_str[16:80]
#     tx_input_asset_id = raw_tx_str[80:144]
    

#     # for i in range(tx_input_amount):

#     return tx

