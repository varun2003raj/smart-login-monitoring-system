# 🔐 Smart Login Monitoring System with Telegram Alerts

## 📌 Overview
This project monitors login activity on a Linux system using `journalctl` and sends real-time alerts to Telegram for suspicious behavior.

---

## 🚀 Features
- Monitors login activity using journalctl
- Detects failed login attempts
- Detects repeated failures (brute-force)
- Sends Telegram alerts
- Detects unknown IP login attempts

---

## 🛠️ Technologies Used
- Python
- Linux (Kali Linux)
- journalctl
- Telegram Bot API

---

## ⚙️ How It Works
- Reads logs using journalctl
- Filters login-related events
- Detects suspicious activity
- Sends alert to Telegram

---

## ▶️ Usage
```bash
sudo python3 login_monitor.py
