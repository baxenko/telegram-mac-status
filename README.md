# Telegram Mac Status Indicator

A lightweight service that automatically updates your Telegram profile emoji based on your Mac's online status.

- **Online (Active):** 🟢
- **Offline (Sleep/Shutdown):** 🔴 (updates after 90 seconds of inactivity)

## How it works

1. **Mac (Client):** Sends a heartbeat (ping) request to the server every 60 seconds.
2. **Server (Docker):** Listens for pings. If no ping is received for >90 seconds, it marks the status as offline and updates the Telegram profile via the API.

## Setup (Server)

1. Rename `.env.example` to `.env` and fill in your Telegram API credentials.
2. Run with Docker Compose:
   ```bash
   docker-compose up -d
