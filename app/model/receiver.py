import hashlib
from app.model.key import *
from app.model import segwit_addr

# get_path_from_index create xpub path from account key index and current address index
# Please attention:
#   account_index_int >= 1
#   address_index_int >= 1
# test data 1:
#   account_index_int: 
#   address_index_int: 
#   path_list: 
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
    # path_list = get_path_from_index(account_index_int, address_index_int, change_bool)
    # child_xpub_str = xpub_to_child_xpub(xpub_str, path_list)
    # child_public_key_str = xpub_to_public_key(child_xpub_str)
    # child_public_key_byte = bytes.fromhex(child_public_key_str)
    
    # ripemd160 = hashlib.new('ripemd160')
    # ripemd160.update(child_public_key_byte)
    public_key_hash_str = control_program_str[4:]
    # control_program_str = '0014' + public_key_hash_str

    if network_str == 'mainnet':
        hrp = 'bm'
    elif network_str == 'testnet':
        hrp = 'tm'
    elif network_str == 'solonet':
        hrp = 'sm'
    address_str = segwit_addr.encode(hrp, 0, bytes.fromhex(public_key_hash_str))

    return address_str