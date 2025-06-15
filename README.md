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
