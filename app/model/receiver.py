import hashlib
from app.model.key import *
from app.model import segwit_addr
import qrcode
import pybase64
from io import BytesIO

# get_path_from_index create xpub path from account key index and current address index
# path: purpose(0x2c=44)/coin_type(btm:0x99)/account_index/change(1 or 0)/address_index
# You can find more details from: https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki
# You can get more test data from: https://gist.github.com/zcc0721/616eaf337673635fa5c9dd5dbb8dd114
# Please attention:
#   account_index_int >= 1
#   address_index_int >= 1
#   change_bool: true or false
# test data 1:
#   account_index_int: 1
#   address_index_int: 1
#   change_bool: true
#   path_list: 2c000000 99000000 01000000 01000000 01000000
# test data 2:
#   account_index_int: 1
#   address_index_int: 1
#   change_bool: false
#   path_list: 2c000000 99000000 01000000 00000000 01000000
# test data 3:
#   account_index_int: 3
#   address_index_int: 1
#   change_bool: false
#   path_list: 2c000000 99000000 03000000 00000000 01000000
def get_path_from_index(account_index_int, address_index_int, change_bool):
    path_list = ['2c000000', '99000000']
    account_index_str = (account_index_int).to_bytes(4, byteorder='little').hex()
    path_list.append(account_index_str)
    if change_bool:
        branch_str = (1).to_bytes(4, byteorder='little').hex()
    else:
        branch_str = (0).to_bytes(4, byteorder='little').hex()
    path_list.append(branch_str)
    address_index_str = (address_index_int).to_bytes(4, byteorder='little').hex()
    path_list.append(address_index_str)
    return {
        "path": path_list
    }


# create_P2WPKH_program create control program
# You can get more test data from: https://gist.github.com/zcc0721/afa12de04b03b9bfc49985a181ebda80
# Please attention:
#   account_index_int >= 1
#   address_index_int >= 1
#   change_bool: true or false
# test data 1:
#   account_index_int: 1
#   address_index_int: 1
#   change_bool: false
#   xpub_str: 3c6664244d2d57168d173c4691dbf8741a67d972b2d3e1b0067eb825e2005d20c5eebd1c26ccad4de5142d7c339bf62cc1fb79a8b3e42a708cd521368dbc9286
#   control_program_str: 0014052620b86a6d5e07311d5019dffa3864ccc8a6bd
# test data 2:
#   account_index_int: 1
#   address_index_int: 1
#   change_bool: true
#   xpub_str: 3c6664244d2d57168d173c4691dbf8741a67d972b2d3e1b0067eb825e2005d20c5eebd1c26ccad4de5142d7c339bf62cc1fb79a8b3e42a708cd521368dbc9286
#   control_program: 001478c3aa31753389fcde04d33d0779bdc2840f0ad4
# test data 3:
#   account_index_int: 1
#   address_index_int: 17
#   change_bool: true
#   xpub_str: 3c6664244d2d57168d173c4691dbf8741a67d972b2d3e1b0067eb825e2005d20c5eebd1c26ccad4de5142d7c339bf62cc1fb79a8b3e42a708cd521368dbc9286
#   control_program: 0014eefb8d0688d7960dfbd79bb3aa1bcaa3ec34415d
# test data 4:
#   account_index_int: 1
#   address_index_int: 1
#   change_bool: false
#   xpub_str: f744493a021b65814ea149118c98aae8d1e217de29fefb7b2024ca341cd834586ee48bbcf1f4ae801ecb8c6784b044fc62a74c58c816d14537e1573c3e20ce79
#   control_program: 001431f2b90b469e89361225aae370f73e5473b9852b
def create_P2WPKH_program(account_index_int, address_index_int, change_bool, xpub_str):
    path_list = get_path_from_index(account_index_int, address_index_int, change_bool)['path']
    child_xpub_str = xpub_to_child_xpub(xpub_str, path_list)['child_xpub']
    child_public_key_str = xpub_to_public_key(child_xpub_str)['public_key']
    child_public_key_byte = bytes.fromhex(child_public_key_str)
    
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(child_public_key_byte)
    public_key_hash_str = ripemd160.hexdigest()
    control_program_str = '0014' + public_key_hash_str
    return {
        "control_program": control_program_str
    }


# create_address create address
# You can get more test data from: https://gist.github.com/zcc0721/8f52d0a80a0a9f964e9d9d9a50e940c5
# Please attention:
#   network_str: mainnet/testnet/solonet
# test data 1:
#   control_program_str: 001431f2b90b469e89361225aae370f73e5473b9852b
#   network_str: mainnet
#   address_str: bm1qx8etjz6xn6ynvy394t3hpae723emnpft3nrwej
# test data 2:
#   control_program_str: 0014eefb8d0688d7960dfbd79bb3aa1bcaa3ec34415d
#   network_str: mainnet
#   address_str: bm1qamac6p5g67tqm77hnwe65x7250krgs2avl0nr6
# test data 3:
#   control_program_str: 0014eefb8d0688d7960dfbd79bb3aa1bcaa3ec34415d
#   network_str: testnet
#   address_str: tm1qamac6p5g67tqm77hnwe65x7250krgs2agfwhrt
# test data 4:
#   control_program_str: 0014d234314ea1533dee584417ecb922f904b8dd6c6b
#   network_str: testnet
#   address_str: tm1q6g6rzn4p2v77ukzyzlktjgheqjud6mrt7emxen
# test data 5:
#   control_program_str: 0014eefb8d0688d7960dfbd79bb3aa1bcaa3ec34415d
#   network_str: solonet
#   address_str: sm1qamac6p5g67tqm77hnwe65x7250krgs2adw9jr5
# test data 6:
#   control_program_str: 0014052620b86a6d5e07311d5019dffa3864ccc8a6bd
#   network_str: solonet
#   address_str: sm1qq5nzpwr2d40qwvga2qval73cvnxv3f4aa9xzh9
def create_address(control_program_str, network_str):
    public_key_hash_str = control_program_str[4:]
    if network_str == 'mainnet':
        hrp = 'bm'
    elif network_str == 'testnet':
        hrp = 'tm'
    else:
        hrp = 'sm'
    address_str = segwit_addr.encode(hrp, 0, bytes.fromhex(public_key_hash_str))
    return {
        "address": address_str
    }

# create_qrcode_base64 create qrcode, then encode it to base64
# type(s) is str
def create_qrcode_base64(s):
    img = qrcode.make(s)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    base64_str = pybase64.b64encode(buffered.getvalue()).decode("utf-8")
    return {
        "base64": base64_str
    }

