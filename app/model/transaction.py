import requests
import json
from _pysha3 import sha3_256
from app.model import receiver

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


'''
get_spend_output_id create tx_input spend output id
test data 1:
  source_id_hexstr: 28b7b53d8dc90006bf97e0a4eaae2a72ec3d869873188698b694beaf20789f21
  asset_id_hexstr: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
  amount_int: 41250000000
  source_position_int: 0
  vmversion_int: 1
  control_program_hexstr: 00149335b1cbd4a77b78e33315a0ed10a95b12e7ca48
  spend_output_id_hexstr: f229ec6f403d586dc87aa2546bbe64c5f7b5f46eb13c6ee4823d03bc88a7cf17
'''
def get_spend_output_id(source_id_hexstr, asset_id_hexstr, amount_int, source_position_int, vmversion_int, control_program_hexstr):
    amount_hexstr = amount_int.to_bytes(8, byteorder='little').hex()
    source_position_hexstr = source_position_int.to_bytes(8, byteorder='little').hex()
    vmversion_hexstr = vmversion_int.to_bytes(8, byteorder='little').hex()
    cp_length_int = len(control_program_hexstr) // 2
    cp_length_hexstr = cp_length_int.to_bytes((cp_length_int.bit_length() + 7) // 8, byteorder='little').hex()
    sc_hexstr = source_id_hexstr + asset_id_hexstr + amount_hexstr + source_position_hexstr + vmversion_hexstr + cp_length_hexstr +  control_program_hexstr
    innerhash_bytes = sha3_256(bytes.fromhex(sc_hexstr)).digest()
    spend_bytes = b'entryid:output1:' + innerhash_bytes
    spend_output_id_hexstr = sha3_256(spend_bytes).hexdigest()
    return spend_output_id_hexstr

'''
get_input_id create tx input_id
test data 1:
    spend_output_id_hexstr: f229ec6f403d586dc87aa2546bbe64c5f7b5f46eb13c6ee4823d03bc88a7cf17
    input_id_hexstr: 6e3f378ed844b143a335e306f4ba26746157589c87e8fc8cba6463c566c56768
'''
def get_input_id(spend_output_id_hexstr):
    innerhash_bytes = sha3_256(bytes.fromhex(spend_output_id_hexstr)).digest()
    input_id_hexstr = sha3_256(b'entryid:spend1:' + innerhash_bytes).hexdigest()
    return input_id_hexstr


# def get_output_id():


'''
decode_raw_tx decode raw transaction
testdata 1:
    raw_tx_str: 070100010161015f28b7b53d8dc90006bf97e0a4eaae2a72ec3d869873188698b694beaf20789f21ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8099c4d5990100011600149335b1cbd4a77b78e33315a0ed10a95b12e7ca48630240897e2d9d24a3b5faaed0579dee7597b401491595675f897504f8945b29d836235bd2fca72a3ad0cae814628973ebcd142d9d6cc92d0b2571b69e5370a98a340c208cb7fb3086f58db9a31401b99e8c658be66134fb9034de1d5c462679270b090702013effffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80f9f8bc98010116001406ce4b689ba026ffd3a7ca65d1d059546d4b78a000013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80c6868f01011600147929ef91997c827bebf60fa608f876ea27523c4700
    network_str: solotnet
    transaction: 
    {
        "status":"success",
        "data":{
            "tx_id":"4f642e0eb1cff2a0bbc085a411a32d74af2f84f9749de0502517b8bebc8ef094",
            "version":1,
            "size":263,
            "time_range":200001,
            "inputs":[
                {
                    "type":"spend",
                    "asset_id":"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                    "asset_definition":{},
                    "amount":101100,
                    "control_program":"0014ddca4dca2cad2781d2002e23a080fe39415b6e54",
                    "address":"tm1qmh9ymj3v45ncr5sq9c36pq8789q4kmj5dzjv54",
                    "spent_output_id":"13c5afc4057758a0ffa43b81e03d79b4929eeb7010fdeb6ca6abd06e93a60669",
                    "input_id":"401519f734c8a0888b3894fcbf01e14818d26492d6d6510233974657a9daf5bf",
                    "witness_arguments":[
                        "629be85f527ff91c503c947e32fb8b35eec8e3b7fe9c45f7da95e081f4bdf3456ffeb203bcf0e6bbd609628bfca774ff797fd515d1ac918feab36f3fa008fc0d",
                        "4b4c18238df718bb957bc4144d7c1472bc185328911ac18c11d655943396e0b2"
                    ]
                }
            ],
            "outputs":[
                {
                    "type":"control",
                    "id":"fb4ced05db7a1872965ba071fdeaf965b669ac7ce08768fa2cfd7c0440691dad",
                    "position":0,
                    "asset_id":"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                    "asset_definition":{

                    },
                    "amount":11,
                    "control_program":"00146baa02b3a7217402e34ff7202ee08795c252956c",
                    "address":"tm1qdw4q9va8y96q9c607uszacy8jhp999tvqqhcm7"
                }
            ],
            "fee":101089
        }
    }
'''
def decode_raw_tx(raw_tx_str, network_str):
    tx = {
        "fee": 0,
        "inputs": [],
        "outputs": [],
        "size": 0,
        "time_range": 0,
        "tx_id": "",
        "version": 0
    }
    tx['fee'] = 0
    tx['size'] = len(raw_tx_str) // 2
    length = 0
    offset = 2
    tx['version'], length = get_uvarint(raw_tx_str[offset:offset+16])
    offset = offset + 2 * length
    tx['time_range'], length = get_uvarint(raw_tx_str[offset:offset+16])
    offset = offset + 2 * length
    tx_input_amount, length = get_uvarint(raw_tx_str[offset:offset+8])
    offset = offset + 2 * length
    for _ in range(tx_input_amount):
        tx_input = {
            "address": "",
            "amount": 0,
            "asset_definition": {},
            "asset_id": "",
            "control_program": "",
            "input_id": "",
            "spent_output_id": "",
            "type": "",
            "witness_arguments": []
        }
        _, length = get_uvarint(raw_tx_str[offset:offset+16])
        offset = offset + 2 * length
        _, length = get_uvarint(raw_tx_str[offset:offset+16])
        offset = offset + 2 * length
        input_type = int(raw_tx_str[offset:offset+2], 16)
        offset += 2
        if input_type == 0:
            pass
        elif input_type == 1:
            tx_input['type'] = "spend"
            _, length = get_uvarint(raw_tx_str[offset:offset+16])
            offset = offset + 2 * length
            source_id = raw_tx_str[offset:offset+64]
            offset += 64
            tx_input['asset_id'] = raw_tx_str[offset:offset+64]
            offset += 64
            tx_input['amount'], length = get_uvarint(raw_tx_str[offset:offset+16])
            offset = offset + 2 * length
            tx['fee'] += tx_input['amount']
            source_positon, length = get_uvarint(raw_tx_str[offset:offset+16])
            offset = offset + 2 * length
            vmversion, length = get_uvarint(raw_tx_str[offset:offset+16])
            offset = offset + 2 * length
            control_program_length, length = get_uvarint(raw_tx_str[offset:offset+16])
            offset = offset + 2 * length
            tx_input['control_program'] = raw_tx_str[offset:offset+2*control_program_length]
            offset = offset + 2 * control_program_length
            tx_input['address'] = receiver.create_address(tx_input['control_program'], network_str)['address']
            _, length = get_uvarint(raw_tx_str[offset:offset+16])
            offset = offset + 2 * length
            witness_arguments_amount, length = get_uvarint(raw_tx_str[offset:offset+16])
            offset = offset + 2 * length
            tx_input['spent_output_id'] = get_spend_output_id(source_id, tx_input['asset_id'], tx_input['amount'], source_positon, vmversion, tx_input['control_program'])
            tx_input['input_id'] = get_input_id(tx_input['spent_output_id'])
            for _ in range(witness_arguments_amount):
                argument_length, length = get_uvarint(raw_tx_str[offset:offset+16])
                offset = offset + 2 * length
                argument = raw_tx_str[offset:offset+2*argument_length]
                offset = offset + 2 * argument_length
                tx_input['witness_arguments'].append(argument)
            tx['inputs'].append(tx_input)
        elif input_type == 2:
            pass
    tx_output_amount, length = get_uvarint(raw_tx_str[offset:offset+16])
    offset = offset + 2 * length
    for i in range(tx_output_amount):
        tx_output = {
            "address": "",
            "amount": 0,
            "asset_definition": {},
            "asset_id": "",
            "control_program": "",
            "id": "",
            "position": 0,
            "type": ""
        }
        tx_output['position'] = i
        _, length = get_uvarint(raw_tx_str[offset:offset+16])
        offset = offset + 2 * length
        _, length = get_uvarint(raw_tx_str[offset:offset+16])
        offset = offset + 2 * length
        tx_output['asset_id'] = raw_tx_str[offset:offset+64]
        offset = offset + 64
        tx_output['amount'], length = get_uvarint(raw_tx_str[offset:offset+16])
        offset = offset + 2 * length
        tx['fee'] -= tx_output['amount']
        _, length = get_uvarint(raw_tx_str[offset:offset+16])
        offset = offset + 2 * length
        control_program_length, length = get_uvarint(raw_tx_str[offset:offset+16])
        offset = offset + 2 * length
        tx_output['control_program'] = raw_tx_str[offset:offset+2*control_program_length]
        offset = offset + 2 * control_program_length
        tx_output['address'] = receiver.create_address(tx_output['control_program'], network_str)['address']
        _, length = get_uvarint(raw_tx_str[offset:offset+16])
        offset = offset + 2 * length
        tx['outputs'].append(tx_output)
    return tx
