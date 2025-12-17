# Telegram Mac Status Indicator 🟢

A Python service that syncs your Mac's online/offline status with your Telegram profile emoji.

- **Online:** Sets your Telegram status/name to 🟢.
- **Offline:** Sets your Telegram status/name to 🔴 (after 90 seconds of inactivity).

## Architecture

1. **Client (macOS):** A background agent (`LaunchAgent`) sends a heartbeat to the server every minute.
2. **Server (Python):** A Flask app listens for heartbeats and updates the Telegram account via Pyrogram.

## 🛠 Server Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
