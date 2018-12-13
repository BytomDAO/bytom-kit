import ed25519

# test data:
#     private_key: 33c6e964cf64246fc37f26be46c7b783ef4364f9d4c69daa4ccd9d0fef5fcef1
#     public_key: b25690a0ccd290a3346fb412dfd342c5ce6134ef116e89b0642d7534e34df432
#     message: hello bytom
#     signature: dfb19c1892796ad9560eb61a065c016c82a7a81a42f2c3f69d20f44582262551b62fee6836c866e008c2cb37bba7e2045013f073ad7f69f5dd2a634929c3d406

def sign(private_key_str, message_str):
    signing_key = ed25519.SigningKey(bytes.fromhex(private_key_str))
    signature = signing_key.sign(message_str.encode(), encoding='hex')
    return signature.decode()

def verify(public_key_str, signature_str, message_str):
    result = False
    verifying_key = ed25519.VerifyingKey(public_key_str.encode(), encoding='hex')
    try:
        verifying_key.verify(signature_str.encode(), message_str.encode(), encoding='hex')
        result = True
    except ed25519.BadSignatureError:
        result = False
    return result