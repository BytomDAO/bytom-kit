import hashlib
from app.model.key import *

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
    if change_bool == True:
        branch_str = (1).to_bytes(4, byteorder='little').hex()
        print("true")
    elif change_bool == False:
        branch_str = (0).to_bytes(4, byteorder='little').hex()
        print("false")
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
    P2WPKH_program_str = '0014' + public_key_hash_str

    return P2WPKH_program_str