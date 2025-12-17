# Telegram Mac Status Indicator 🟢

A lightweight Python service that automatically updates your Telegram profile emoji based on your Mac's status.

- **Online:** Sets status to 🟢.
- **Offline:** Sets status to 🔴 (after 90 seconds of inactivity).

## How it works

1. **Mac (Client):** Uses a native `LaunchAgent` to send a heartbeat (ping) to the server every minute.
2. **Server (Python):** Listens for pings. If no ping is received, it updates the Telegram profile via API.

## Installation

### 1. Server Side (Python)

Clone the repo and install dependencies:

    pip install -r requirements.txt

Configure `.env` file (see `.env.example`) and run the server:

    python server.py

### 2. Client Side (macOS)

Create a plist file at `~/Library/LaunchAgents/com.telegram.status.plist`.

Paste this content (replace `YOUR_SERVER_IP` and `YOUR_SECRET_TOKEN`):

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>Label</key>
        <string>com.telegram.status</string>
        <key>ProgramArguments</key>
        <array>
            <string>/usr/bin/curl</string>
            <string>-s</string>
            <string>http://YOUR_SERVER_IP:5050/ping?token=YOUR_SECRET_TOKEN</string>
        </array>
        <key>StartInterval</key>
        <integer>60</integer>
        <key>RunAtLoad</key>
        <true/>
    </dict>
    </plist>

Load the agent:

    launchctl load ~/Library/LaunchAgents/com.telegram.status.plist
