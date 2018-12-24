import random
import hashlib
import pbkdf2
import hmac
import ed25519
from app.model.signature import *

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


# s_str must be >= 32 bytes long and gets rewritten in place.
# This is NOT the same pruning as in Ed25519: it additionally clears the third
# highest bit to ensure subkeys do not overflow the second highest bit.
def prune_root_scalar(s_str):
    s_0_int = int.from_bytes(bytes.fromhex(s_str[0:2]), byteorder='big') & 248
    s_0_str = "%0.2x" % s_0_int
    new_s_str = s_0_str + s_str[2:]
    s_31_int = int.from_bytes(bytes.fromhex(new_s_str[62:64]), byteorder='big') & 31
    s_31_str = "%0.2x" % s_31_int
    new_s_str = new_s_str[:62] + s_31_str + new_s_str[64:]
    s_31_int = int.from_bytes(bytes.fromhex(new_s_str[62:64]), byteorder='big') | 64
    s_31_str = "%0.2x" % s_31_int
    new_s_str = new_s_str[:62] + s_31_str + new_s_str[64:]
    
    return new_s_str


# seed_to_root_xprv create rootxprv from seed
# seed_str length is 512 bits.
# root_xprv length is 512 bits.
# You can verify or get more test data from: https://gist.github.com/zcc0721/0aa1b971f4bf93d8f67e25f57b8b97ee
# test data 1:
#   seed_str: afa3a86bbec2f40bb32833fc6324593824c4fc7821ed32eac1f762b5893e56745f66a6c6f2588b3d627680aa4e0e50efd25065097b3daa8c6a19d606838fe7d4
#   root_xprv_str: 302a25c7c0a68a83fa043f594a2db8b44bc871fced553a8a33144b31bc7fb84887c9e75915bb6ba3fd0b9f94a60b7a5897ab9db6a48f888c2559132dba9152b0
# test data 2:
#   seed_str: b435f948bd3748ede8f9d6f59728d669939e79c6c885667a5c138e05bbabde1de0dcfcbe0c6112022fbbf0da522f4e224a9c2381016380688b51886248b3156f
#   root_xprv_str: 6032adeb967ac5ccbf988cf8190817bf9040c8cfd9cdfe3d5e400effb2946946d478b61cc6be936f367ae769eb1dc65c473ee73cac2eb43cf6d5e7c62b7f0062
# test data 3:
#   seed_str: ecc2bbb6c0492873cdbc81edf56bd896d3b644047879840e357be735b7fa7b6f4af1be7b8d71cc649ac4ca3816f9ccaf11bf49f4effb845f3c19e16eaf8bfcda
#   root_xprv_str: a01d6b741b0e74b8d0836ac22b675bbf8e108148ef018d1b000aef1a899a134bd316c0f59e7333520ae1a429504073b2773869e95aa95bb3a4fa0ec76744025c
def seed_to_root_xprv(seed_str):
    hc_str = hmac.HMAC(b'Root', bytes.fromhex(seed_str), digestmod=hashlib.sha512).hexdigest()
    root_xprv_str = prune_root_scalar(hc_str[:64]) + hc_str[64:]

    return root_xprv_str


##################################################
# def xprv_to_xpub(xprv_str):
# private_key = ed25519.SigningKey(bytes.fromhex(xprv_str[:64]))
# public_key = private_key.get_verifying_key().to_ascii(encoding='hex')
# xpub_str = public_key.decode() + xprv_str[64:]
#     return xpub_str
##################################################


# def xprv_to_child_xprv(xprv_str, path_str):
#     child_xprv_str = xprv_str
#     return child_xprv_str

# xprv_to_expanded_private_key create expanded private key from xprv
# You can verify or get more test data from: https://gist.github.com/zcc0721/ef0bf2e69f5e92b29d716981f2a8fe7d
# test data 1:
#   xprv_str: 406c82307bf7978d17f3ecfeea7705370e9faef2027affa86c8027c6e11a8a50e231e65bd97048850ae6c39d0f46b63ae70aa24f5aac7877727c430c2201e6d6
#   expanded_private_key_str_xprv: 406c82307bf7978d17f3ecfeea7705370e9faef2027affa86c8027c6e11a8a50d828bf44b1a109c2bbb4c72685858e2f2ab8b405beef1e4ecc12d1ed8511e8eb
# test data 2:
#   xprv_str: 6032adeb967ac5ccbf988cf8190817bf9040c8cfd9cdfe3d5e400effb2946946d478b61cc6be936f367ae769eb1dc65c473ee73cac2eb43cf6d5e7c62b7f0062
#   expanded_private_key_str_xprv: 6032adeb967ac5ccbf988cf8190817bf9040c8cfd9cdfe3d5e400effb2946946ddbb71e7a76595c6bc24937d76085d24315713764cbdf1364ab9091953009cd8
# test data 3:
#   xprv_str: 509a095ad862322641b8d66e84561aae1d4816045167e2c4dfadf464928e114300c0a162d41c0cdf196d61f4492f546e50bfff253b9d5d930d1bb89197cd333d
#   expanded_private_key_str_xprv: 509a095ad862322641b8d66e84561aae1d4816045167e2c4dfadf464928e11432787f5e10f9598f80fb41e4a648b609463c06e625641366f3279658b2b0f5268
def xprv_to_expanded_private_key(xprv_str):
    hc_str = hmac.HMAC(b'Expand', bytes.fromhex(xprv_str), digestmod=hashlib.sha512).hexdigest()
    expanded_private_key_str = xprv_str[:64] + hc_str[64:]

    return expanded_private_key_str


# xpub_to_public_key create 32 bytes public key from xpub
# xpub length is 64 bytes.
# You can verify or get more test data from: https://gist.github.com/zcc0721/9e10f2fa5bd0c8f33aa6dfc87f6aa856
# test data 1:
#   xpub_str: ecc2bbb6c0492873cdbc81edf56bd896d3b644047879840e357be735b7fa7b6f4af1be7b8d71cc649ac4ca3816f9ccaf11bf49f4effb845f3c19e16eaf8bfcda
#   public_key_str: ecc2bbb6c0492873cdbc81edf56bd896d3b644047879840e357be735b7fa7b6f
# test data 2:
#   xpub_str: 406c82307bf7978d17f3ecfeea7705370e9faef2027affa86c8027c6e11a8a50e231e65bd97048850ae6c39d0f46b63ae70aa24f5aac7877727c430c2201e6d6
#   public_key_str: 406c82307bf7978d17f3ecfeea7705370e9faef2027affa86c8027c6e11a8a50
# test data 3:
#   xpub_str: b435f948bd3748ede8f9d6f59728d669939e79c6c885667a5c138e05bbabde1de0dcfcbe0c6112022fbbf0da522f4e224a9c2381016380688b51886248b3156f
#   public_key_str: b435f948bd3748ede8f9d6f59728d669939e79c6c885667a5c138e05bbabde1d
def xpub_to_public_key(xpub_str):
    public_key_str = xpub_str[:64]

    return public_key_str


# def xprv_sign(xprv_str, message_str):
#     expanded_private_key = xprv_to_expanded_private_key(xprv_str)

#     return signature_str
    

# xpub_verify verify signature
# xpub_str length is 64 bytes.
# message_str length is variable.
# signature_str length is 64 bytes.
# You can verify or get more test data from: https://gist.github.com/zcc0721/61a26c811a632623678e274cc7e5c10b
# test data 1:
#   xprv_str: c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c
#   xpub_str: 1b0541a7664cee929edb54d9ef21996b90546918a920a77e1cd6015d97c56563d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c
#   message_str: a6ce34eec332b32e42ef3407e052d64ac625da6f
#   signature_str: f02f5bb22d8b32f14e88059a786379c26256892f45cf64770c844d0c5de2e52c00307b7bb25fcbb18be13c339a2f511a7c015a8cf81ac681052efe8e50eff00e
# test data 2:
#   xprv_str: 008ce51e3b52ee03eb0ad96c55eb5c9fe8736410518b585a0b7f35b2ab48d24c166364ce19322721b7dec84442c3665d97d0e995ba4d01c0f4b19b841379ac90
#   xpub_str: ead6415a077b91aa7de32e1cf63350f9351d0298f5accc2cf92ef9429bd1f86c166364ce19322721b7dec84442c3665d97d0e995ba4d01c0f4b19b841379ac90
#   message_str: 68656c6c6f206279746f6d      # value is: 'hello bytom'
#   signature_str: 1cc6b0f4031352ffd7a62540f13edddaaebf2df05db7a4926df5513129a8e85dcff1324545a024b16f958239ea67840ced3c2d57bb468dbf0e6cf1d1075f0b0f
# test data 3:
#   xprv_str: 88c0c40fb54ef9c1b90af8cce8dc4c9d54f915074dde93f79ab61cedae03444101ff37ac4a07869214c2735bba0175e001abe608db18538e083e1e44430a273b
#   xpub_str: cb22ce197d342d6bb440b0bf13ddd674f367275d28a00f893d7f0b10817690fd01ff37ac4a07869214c2735bba0175e001abe608db18538e083e1e44430a273b
#   message_str: 1246b84985e1ab5f83f4ec2bdf271114666fd3d9e24d12981a3c861b9ed523c6
#   signature_str: ab18f49b23d03295bc2a3f2a7d5bb53a2997bed733e1fc408b50ec834ae7e43f7da40fe5d9d50f6ef2d188e1d27f976aa2586cef1ba00dd098b5c9effa046306
def xpub_verify(xpub_str, message_str, signature_str):
    result = False
    result = verify(xpub_to_public_key(xpub_str), signature_str, message_str)

    return result