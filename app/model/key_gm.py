import hmac
import hashlib

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