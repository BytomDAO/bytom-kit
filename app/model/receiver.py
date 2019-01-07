import hashlib
from app.model.key import *
from app.model import segwit_addr

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

    return path_list


def create_P2WPKH_program(account_index_int, address_index_int, change_bool, xpub_str):
    path_list = get_path_from_index(account_index_int, address_index_int, change_bool)
    child_xpub_str = xpub_to_child_xpub(xpub_str, path_list)
    child_public_key_str = xpub_to_public_key(child_xpub_str)
    child_public_key_byte = bytes.fromhex(child_public_key_str)
    
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(child_public_key_byte)
    public_key_hash_str = ripemd160.hexdigest()
    control_program_str = '0014' + public_key_hash_str

    return control_program_str


def create_address(control_program_str, network_str):
    public_key_hash_str = control_program_str[4:]
    if network_str == 'mainnet':
        hrp = 'bm'
    elif network_str == 'testnet':
        hrp = 'tm'
    else:
        hrp = 'sm'
    address_str = segwit_addr.encode(hrp, 0, bytes.fromhex(public_key_hash_str))

    return address_str