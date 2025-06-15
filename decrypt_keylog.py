import base64
import json
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes, hmac

# 32-byte key must be the SAME as used during encryption
KEY = b'\x00'*32  # TODO: put your actual key here

log_file = "keylog_encrypted.txt"

def decrypt_and_verify(record_json: str) -> str:
    """Decrypt and verify HMAC of a single encrypted record."""
    record = json.loads(record_json)
    nonce = base64.b64decode(record['nonce'])
    ct = base64.b64decode(record['ct'])
    hmac_tag = base64.b64decode(record['hmac'])

    # First, verify HMAC
    h = hmac.HMAC(KEY, hashes.SHA256()) 
    h.update(nonce + ct) 
    try:
        h.verify(hmac_tag) 
    except Exception:
        return "[TAMPERED OR CORRUPTED]"

    # If HMAC checks, decrypt
    aesgcm = AESGCM(KEY)
    plaintext = aesgcm.decrypt(nonce, ct, None)
    return plaintext.decode('utf-8')

def main():
    if not os.path.exists(log_file):
        print("Log file not found.")
        return
    
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            message = decrypt_and_verify(line)
            print(message)

if __name__ == "__main__":
    main()
