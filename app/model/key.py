import random
import hashlib
import pbkdf2
import hmac
import ed25519

# create_key create 128 bits entropy
def create_entropy():
    hex_str = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    entropy_str = ""
    for _ in range(32):
        # create interger in range [1,15]
        num = random.randint(0,15)
        entropy_str += hex_str[num]

    return entropy_str

# entropy_to_mnemonic create mnemonic from 128 bits entropy(the entropy_str length is 32)
# return 12 mnemonics
# verify or get more test data, please ref: https://gist.github.com/zcc0721/63aeb5143807950f7b7051fadc08cef0
# test data 1:
#   entropy_str: 1db8b283eb4623e749732a341396e0c9
#   mnemonic_str: buffalo sheriff path story giraffe victory chair grab cross original return napkin
# test data 2:
#   entropy_str: 4d33735a9e92f634d22aecbb4044038d
#   mnemonic_str: essay oppose stove diamond control bounce emerge frown robust acquire abstract brick
# test data 3:
#   entropy_str: 089fe9bf0cac76760bc4b131d938669e
#   mnemonic_str: ancient young hurt bone shuffle deposit congress normal crack six boost despair
def entropy_to_mnemonic(entropy_str):
    mnemonic_str = ""
    mnemonic_length = 12

    # create a 12 elements mnemonic_list 
    mnemonic_list = []
    for _ in range(mnemonic_length):
        mnemonic_list.append('')

    entropy_bytes = bytes.fromhex(entropy_str)
    checksum = hashlib.sha256(entropy_bytes).hexdigest()[:1]
    new_entropy_str = "0" + entropy_str + checksum
    new_entropy_bytes = bytes.fromhex(new_entropy_str)
    new_entropy_int = int.from_bytes(new_entropy_bytes, byteorder='big')

    file = open('./app/model/english_mnemonic.txt', mode='r')
    word_list = file.readlines()
    file.close()

    for i in range(11, -1, -1):
        word_index = new_entropy_int % 2048
        new_entropy_int = new_entropy_int >> 11
        mnemonic_list[i] = word_list[word_index]

    for i in range(12):
        mnemonic_str += mnemonic_list[i][:-1]
        mnemonic_str += " "

    return mnemonic_str[:-1]

# mnemonic_to_seed create seed from mnemonic
# You can find more details from: https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki#from-mnemonic-to-seed
# You can verify or get more test data from: https://gist.github.com/zcc0721/4918e891073a9ca6c444ec7490298e82
# test data 1:
#   mnemonic_str: ancient young hurt bone shuffle deposit congress normal crack six boost despair
#   seed_str: afa3a86bbec2f40bb32833fc6324593824c4fc7821ed32eac1f762b5893e56745f66a6c6f2588b3d627680aa4e0e50efd25065097b3daa8c6a19d606838fe7d4
# test data 2:
#   mnemonic_str: rich decrease live pluck friend recipe burden minor similar agent tired horror
#   seed_str: b435f948bd3748ede8f9d6f59728d669939e79c6c885667a5c138e05bbabde1de0dcfcbe0c6112022fbbf0da522f4e224a9c2381016380688b51886248b3156f
# test data 3:
#   mnemonic_str: enough ginger just mutual fit trash loop mule peasant lady market hub
#   seed_str: ecc2bbb6c0492873cdbc81edf56bd896d3b644047879840e357be735b7fa7b6f4af1be7b8d71cc649ac4ca3816f9ccaf11bf49f4effb845f3c19e16eaf8bfcda
def mnemonic_to_seed(mnemonic_str):
    password_str = mnemonic_str
    salt_str = "mnemonic"
    seed_str = pbkdf2.PBKDF2(password_str, salt_str, iterations=2048, digestmodule=hashlib.sha512, macmodule=hmac).hexread(64)

    return seed_str

# seed_to_root_xprv create rootxprv from seed
# seed_str length is 512 bits.
# root_xprv length is 512 bits.
# You can verify or get more test data from: https://gist.github.com/zcc0721/0aa1b971f4bf93d8f67e25f57b8b97ee
# test data 1:
#   seed_str: afa3a86bbec2f40bb32833fc6324593824c4fc7821ed32eac1f762b5893e56745f66a6c6f2588b3d627680aa4e0e50efd25065097b3daa8c6a19d606838fe7d4
#   root_xprv: 302a25c7c0a68a83fa043f594a2db8b44bc871fced553a8a33144b31bc7fb84887c9e75915bb6ba3fd0b9f94a60b7a5897ab9db6a48f888c2559132dba9152b0
# test data 2:
#   seed_str: b435f948bd3748ede8f9d6f59728d669939e79c6c885667a5c138e05bbabde1de0dcfcbe0c6112022fbbf0da522f4e224a9c2381016380688b51886248b3156f
#   root_xprv: 6032adeb967ac5ccbf988cf8190817bf9040c8cfd9cdfe3d5e400effb2946946d478b61cc6be936f367ae769eb1dc65c473ee73cac2eb43cf6d5e7c62b7f0062
# test data 3:
#   seed_str: ecc2bbb6c0492873cdbc81edf56bd896d3b644047879840e357be735b7fa7b6f4af1be7b8d71cc649ac4ca3816f9ccaf11bf49f4effb845f3c19e16eaf8bfcda
#   root_xprv: a01d6b741b0e74b8d0836ac22b675bbf8e108148ef018d1b000aef1a899a134bd316c0f59e7333520ae1a429504073b2773869e95aa95bb3a4fa0ec76744025c
def seed_to_root_xprv(seed_str):
    hc_str = hmac.HMAC(b'Root', bytes.fromhex(seed_str), digestmod=hashlib.sha512).hexdigest()
    hc_0_int = int.from_bytes(bytes.fromhex(hc_str[0:2]), byteorder='big') & 248
    hc_0_str = "%0.2x" % hc_0_int
    new_hc_str = hc_0_str + hc_str[2:]
    hc_31_int = int.from_bytes(bytes.fromhex(new_hc_str[62:64]), byteorder='big') & 31
    hc_31_str = "%0.2x" % hc_31_int
    new_hc_str = new_hc_str[:62] + hc_31_str + new_hc_str[64:]
    hc_31_int = int.from_bytes(bytes.fromhex(new_hc_str[62:64]), byteorder='big') | 64
    hc_31_str = "%0.2x" % hc_31_int
    new_hc_str = new_hc_str[:62] + hc_31_str + new_hc_str[64:]
    root_xprv_str = new_hc_str

    return root_xprv_str

# def xprv_to_xpub(xprv_str):
# private_key = ed25519.SigningKey(bytes.fromhex(xprv_str[:64]))
# public_key = private_key.get_verifying_key().to_ascii(encoding='hex')
# xpub_str = public_key.decode() + xprv_str[64:]
#     return xpub_str

