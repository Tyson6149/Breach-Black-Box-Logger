# Breach-Black-Box-Logger
Developed a lightweight, tamper-evident keylogger with AES-256-GCM encryption and HMAC-based integrity checks for post-breach forensic investigations. Implemented persistent, stealthy logging with process and timestamp context. Designed a PyQt5 GUI for secure log management and forensic analysis.

# 🔐 Post-Breach Black Box Logger (Encrypted, Tamper-Evident Keylogger)

A lightweight, user-mode keylogger designed for **post-breach forensic analysis**. It securely captures keystrokes with contextual metadata (active window + process), encrypts each entry with **AES-256-GCM**, and signs it with **HMAC-SHA256** to ensure integrity.

---

## 🎯 Purpose

This tool helps incident response teams reconstruct attacker behavior **after a breach**. It balances privacy, security, and simplicity—ideal for individual systems or small organizations without full EDR.

---

## 🧰 Features

- ✅ Captures keystrokes with timestamps, active window title, and process name  
- 🔒 AES-256-GCM encryption for confidentiality  
- 🧾 HMAC-SHA256 for tamper detection  
- 📄 Stores logs as base64-encoded JSON lines  
- 🧠 Simple persistence (Startup folder shortcut)  
- ⌨️ Stops gracefully on `ESC` key press  
- 🧪 Decryption/verification script included

---

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
pip install pynput cryptography pywin32 psutil
````

### 2. Generate and Set Environment Variables

Use Python to generate 32-byte base64 keys:

```python
import base64, os
print("AES_KEY =", base64.b64encode(os.urandom(32)).decode())
print("HMAC_KEY =", base64.b64encode(os.urandom(32)).decode())
```

Then set them (temporary):

```bash
set KEYLOGGER_AES_KEY=your_base64_aes_key
set KEYLOGGER_HMAC_KEY=your_base64_hmac_key
```

Or add them permanently via **System > Environment Variables**.

---

## ▶️ Running the Logger

```bash
python keylogger_encrypted.py
```

> Press `ESC` to stop the logger. Logs are saved in `keylog_encrypted.txt`.

---

## 🔍 Decrypting & Verifying Logs

```bash
python decrypt_keylog.py
```

This script:

* Verifies HMAC-SHA256 signatures
* Decrypts each entry
* Prints human-readable results

---

## 📂 Folder Structure

```plaintext
keyloggerproject/
├── keylogger_encrypted.py       # Main logger script
├── decrypt_keylog.py            # Log decryption/verification tool
├── keylog_encrypted.txt         # Encrypted log file
├── README.md                    # Project overview
├── requirements.txt             # Python dependencies
└── report.pdf                   # Final internship report
```

---

## 🛡 Security Model

| Property         | How it's Handled                 |
| ---------------- | -------------------------------- |
| Confidentiality  | AES-GCM encryption (256-bit key) |
| Integrity        | HMAC-SHA256 with secret key      |
| Tamper Detection | Verified during decryption       |

---

## 🚀 Future Enhancements

* GUI viewer & control panel
* Secure key storage (e.g., Windows Credential Vault)
* Log rotation & size limits
* Threat intel integration

---

## 📜 License

For educational and ethical research purposes only. Do **not** deploy in production or monitoring scenarios without proper legal clearance.

```
