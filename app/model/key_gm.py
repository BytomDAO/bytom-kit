import hmac
import hashlib
from gmssl import sm2, func
import random
from app.model import pn

# get_gm_root_xprv create rootxprv from seed
# seed_str length is 512 bits.
# root_xprv length is 512 bits.
# You can get more test data from: https://gist.github.com/zcc0721/8bfc1e1c92b7cd9f00743d6878097809
# test data 1:
#   seed_str: ecc2bbb6c0492873cdbc81edf56bd896d3b644047879840e357be735b7fa7b6f4af1be7b8d71cc649ac4ca3816f9ccaf11bf49f4effb845f3c19e16eaf8bfcda
#   root_xprv_str: a61d6b741b0e74b8d0836ac22b675bbf8e108148ef018d1b000aef1a899a136bd316c0f59e7333520ae1a429504073b2773869e95aa95bb3a4fa0ec76744025c
# test data 2:
#   seed_str: afa3a86bbec2f40bb32833fc6324593824c4fc7821ed32eac1f762b5893e56745f66a6c6f2588b3d627680aa4e0e50efd25065097b3daa8c6a19d606838fe7d4
#   root_xprv_str: 302a25c7c0a68a83fa043f594a2db8b44bc871fced553a8a33144b31bc7fb88887c9e75915bb6ba3fd0b9f94a60b7a5897ab9db6a48f888c2559132dba9152b0
# test data 3:
#   seed_str: b435f948bd3748ede8f9d6f59728d669939e79c6c885667a5c138e05bbabde1de0dcfcbe0c6112022fbbf0da522f4e224a9c2381016380688b51886248b3156f
#   root_xprv_str: 6532adeb967ac5ccbf988cf8190817bf9040c8cfd9cdfe3d5e400effb29469e6d478b61cc6be936f367ae769eb1dc65c473ee73cac2eb43cf6d5e7c62b7f0062
def get_gm_root_xprv(seed_str):
    hc_str = hmac.HMAC(b'Root', bytes.fromhex(seed_str), digestmod=hashlib.sha512).hexdigest()
    root_xprv_str = hc_str
    return {
        "root_xprv": root_xprv_str
    }


# get_gm_xpub derives new xpub from xprv
# xprv length is 64 bytes.
# xpub length is 65 bytes.
# You can get more test data from: https://gist.github.com/zcc0721/9e5761e6a924cce3aa7cf7f72721218a
# test data 1:
#   xprv_str: c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c
#   xpub_str: 02476044353971ae0ed41cba76f27d0bd2e09d09db5c238bb74f69569bf343f742d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c
# test data 2:
#   xprv_str: 36667587de27eec684fc4b222276f22a24d9a82e947ee0119148bedd4dec461dd4e1b1d95dfb0f78896677ea1026af7510b41fabd3bd5771311c0cb6968337b2
#   xpub_str: 0396a36cd902db56eca016c213a8ac25de35a7afd78061351f1898529f0956c22ed4e1b1d95dfb0f78896677ea1026af7510b41fabd3bd5771311c0cb6968337b2
# test data 3:
#   xprv_str: 74a49c698dbd3c12e36b0b287447d833f74f3937ff132ebff7054baa18623c35a705bb18b82e2ac0384b5127db97016e63609f712bc90e3506cfbea97599f46f
#   xpub_str: 03cafbdedea4a639d31fe4c257f1bb58303359be1a00b9f90b5c605f57e4308ed1a705bb18b82e2ac0384b5127db97016e63609f712bc90e3506cfbea97599f46f
def get_gm_xpub(xprv_str):
    private_key_int = int(xprv_str[:64], 16)
    sm2_crypt = sm2.CryptSM2(private_key=xprv_str[:64], public_key="")
    public_key_str = sm2_crypt._kg(private_key_int, sm2.default_ecc_table['g'])
    pc = '0' + str(int(public_key_str[-1], 16) % 2 + 2)
    xpub_str = pc + public_key_str[:64] + xprv_str[64:]
    return {
        "xpub": xpub_str
    }


# get_gm_xprv create expanded private key from xprv
# You can get more test data from: https://gist.github.com/zcc0721/ef0bf2e69f5e92b29d716981f2a8fe7d
# test data 1:
#   xprv_str: 406c82307bf7978d17f3ecfeea7705370e9faef2027affa86c8027c6e11a8a50e231e65bd97048850ae6c39d0f46b63ae70aa24f5aac7877727c430c2201e6d6
#   expanded_private_key_str_xprv: 406c82307bf7978d17f3ecfeea7705370e9faef2027affa86c8027c6e11a8a50d828bf44b1a109c2bbb4c72685858e2f2ab8b405beef1e4ecc12d1ed8511e8eb
# test data 2:
#   xprv_str: 6032adeb967ac5ccbf988cf8190817bf9040c8cfd9cdfe3d5e400effb2946946d478b61cc6be936f367ae769eb1dc65c473ee73cac2eb43cf6d5e7c62b7f0062
#   expanded_private_key_str_xprv: 6032adeb967ac5ccbf988cf8190817bf9040c8cfd9cdfe3d5e400effb2946946ddbb71e7a76595c6bc24937d76085d24315713764cbdf1364ab9091953009cd8
# test data 3:
#   xprv_str: 509a095ad862322641b8d66e84561aae1d4816045167e2c4dfadf464928e114300c0a162d41c0cdf196d61f4492f546e50bfff253b9d5d930d1bb89197cd333d
#   expanded_private_key_str_xprv: 509a095ad862322641b8d66e84561aae1d4816045167e2c4dfadf464928e11432787f5e10f9598f80fb41e4a648b609463c06e625641366f3279658b2b0f5268
def get_gm_xprv(xprv_str):
    hc_str = hmac.HMAC(b'Expand', bytes.fromhex(xprv_str), digestmod=hashlib.sha512).hexdigest()
    expanded_private_key_str = xprv_str[:64] + hc_str[64:]
    return {
        "expanded_private_key": expanded_private_key_str
    }


# get_gm_public_key create 33 bytes public key from xpub
# xpub length is 65 bytes.
# You can get more test data from: https://gist.github.com/zcc0721/e159677bf776fe0209bca5b890cb87c3
# test data 1:
#   xpub_str: 03c74f3a946940d43e0f8c6da40680c0078e6e1008ca6ea869d57536c31b7ede20adc168c3698fa538fa587c4e519d1eb7a2593f178bfe0c93890a0f09e1634607
#   public_key_str: 03c74f3a946940d43e0f8c6da40680c0078e6e1008ca6ea869d57536c31b7ede20
# test data 2:
#   xpub_str: 02914d51fcc3b90a87ffe3424995a9db8757a9d67812edd85207c47edc9f7f34e368684ae4d706f68c710fe1dbd20d73a8faaaf34966678a5d58486ac193a851ca
#   public_key_str: 02914d51fcc3b90a87ffe3424995a9db8757a9d67812edd85207c47edc9f7f34e3
# test data 3:
#   xpub_str: 03603b2eb079257513d253a92ad45ce5ef12cc285dd8c13fc77c95844468f5eb4482f33c577c3a71ac733136b17d68b65a184b225431ab658555735e436fdb13e6
#   public_key_str: 03603b2eb079257513d253a92ad45ce5ef12cc285dd8c13fc77c95844468f5eb44
def get_gm_public_key(xpub_str):
    public_key_str = xpub_str[:66]
    return {
        "public_key": public_key_str
    }


# get_gm_child_xprv create new xprv through the path
# xprv_str length is 64 bytes.
# path_list item is hex string.
# child_xprv length is 64 bytes.
# You can get more test data from: https://gist.github.com/zcc0721/db45d25d3432806ff33dcd87f694588b
# test data 1:
#   xprv_str: 10fdbc41a4d3b8e5a0f50dd3905c1660e7476d4db3dbd9454fa4347500a633531c487e8174ffc0cfa76c3be6833111a9b8cd94446e37a76ee18bb21a7d6ea66b
#   path_list: 010400000000000000
#   path_list: 0100000000000000
#   child_xprv_str: 042f319fc7ae020937c0191294f6298b07e0f2acd01621f3ba25b2edc51b5098fde8c077dc7110da22251db1779b9a36fd92acbf559ef6fb170126074453f0a2
# test data 2:
#   xprv_str: c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c
#   path_list: 00
#   path_list: 00
#   child_xprv_str: 838159f7bcad836cc0bb5727eb446e5b989c90dd6084c723746188e84f8405f2f305b60bd191053e84aac16a91380dd67889b203c3f920a5ef06b2cb03cc0ae7
# test data 3:
#   xprv_str: c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c
#   path_list: 010203
#   path_list: 7906a1
#   child_xprv_str: ff7fc1c5a34fbeb739f8ac77ea7728685e7a9c29048e16bde69112ecff4a9aad4f9ee5721fce2d638071bcc1e2ee7ba470cb49d6356fdcf24127a28c09558b55
def get_gm_child_xprv(xprv_str, path_list):
    for i in range(len(path_list)):
        selector_bytes = bytes.fromhex(path_list[i])
        xpub_str = get_gm_xpub(xprv_str)['xpub']
        xpub_bytes = bytes.fromhex(xpub_str)
        xprv_bytes = bytes.fromhex(xprv_str)
        hc_bytes = hmac.HMAC(xpub_bytes[33:], b'N'+xpub_bytes[:33]+selector_bytes, digestmod=hashlib.sha512).digest()
        left_int = int(hc_bytes[:32].hex(), 16)
        private_key_int = int(xprv_bytes[:32].hex(), 16)
        sm2_n_str = 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123'
        sm2_n_int = int(sm2_n_str, 16)
        child_key_int = (left_int + private_key_int) % sm2_n_int
        child_key_str = (child_key_int).to_bytes(32, byteorder='big').hex()
        xprv_str = child_key_str + hc_bytes[32:].hex()
    child_xprv_str = xprv_str
    return {
        "child_xprv": child_xprv_str
    }


# decompress_public_key calculate y 
# dec_pubkey_str length is 33 bytes.
# You can get more test data from: 
# test data 1:
#   xpub_str: 02e097442c49eccae999f7687e088c918838df8d804980a220dba6bd7a51258e76347a32ad977251122e50456dcfe155d80cbfa83186a64f7756f044a126e664ac
#   y_str: f8ac4140ec52355bc699e3b21a87d7824db5443f33641aed14e2e603491b43b4
# test data 2:
#   xpub_str: 02476044353971ae0ed41cba76f27d0bd2e09d09db5c238bb74f69569bf343f742d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c
#   y_str: 76d809326d28a80900db49341731ef43c2791d8ef34d98803252a47fbb0b4e96
# test data 3:
#   xpub_str: 03c74f3a946940d43e0f8c6da40680c0078e6e1008ca6ea869d57536c31b7ede20adc168c3698fa538fa587c4e519d1eb7a2593f178bfe0c93890a0f09e1634607
#   y_str: 4c12dc51fed482f03b277163fe551178f5a7059e8384236c9e4e614b90afeee1
def decompress_public_key(dec_pubkey_str):
    p_int = int('FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF', 16)
    a_int = int('FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC', 16)
    b_int = int('28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93', 16)
    x_int = int(dec_pubkey_str[2:66], 16)
    ysq = (x_int **3 + a_int * x_int + b_int) % p_int
    y1, y2 = pn.sqrt2(ysq, p_int)
    if y1 & 1 == 1:
        y1, y2 = y2, y1
    if dec_pubkey_str[:2] == '02':
        y = y1
    else:
        y = y2
    y_str = (y).to_bytes(32, byteorder='big').hex()
    return y_str



# def gm_xprv_sign(xprv_str, message_str):
#     sm2_crypt = sm2.CryptSM2(private_key=xprv_str[:64], public_key="")
#     K = random.randint(0, 2**256)
#     K_str = K.to_bytes(32, byteorder='big').hex()
#     data = bytes.fromhex(message_str)
#     sig = sm2_crypt.sign(data, K_str)
#     return sig
#     # print(sig)
#     # xprv_str = get_gm_xprv(xprv_str)['expanded_private_key']
#     # xprv_bytes = bytes.fromhex(xprv_str)
#     # message_bytes = bytes.fromhex(message_str)
#     # data_bytes = xprv_bytes[32:64]


# def gm_xpub_verify(xpub_str, message_str, signature_str):
#     public_key = xpub_str[:66]
#     result = False
#     sm2_crypt = sm2.CryptSM2(private_key="", public_key=public_key)
#     data = bytes.fromhex(message_str)
#     result = sm2_crypt.verify(signature_str, data)
#     return {
#         "result": result
#     }