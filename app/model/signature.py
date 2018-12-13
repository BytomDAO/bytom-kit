import ed25519

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