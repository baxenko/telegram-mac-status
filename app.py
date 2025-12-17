import os
import time
import threading
from flask import Flask, request
from pyrogram import Client
from datetime import datetime

app = Flask(__name__)

# Configuration
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")
PING_TOKEN = os.getenv("PING_TOKEN")
ONLINE_EMOJI = os.getenv("ONLINE_EMOJI", "🟢")
OFFLINE_EMOJI = os.getenv("OFFLINE_EMOJI", "🔴")

# State
last_ping_time = time.time()
current_status = "online"  # online / offline

# Initialize Telegram Client
client = Client("session", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE)

def update_telegram_status(status):
    """Updates the emoji in the Telegram profile."""
    try:
        emoji = ONLINE_EMOJI if status == "online" else OFFLINE_EMOJI
        with client:
            client.update_profile(last_name=emoji)
        print(f"[{datetime.now()}] Status updated to: {status} {emoji}")
    except Exception as e:
        print(f"[{datetime.now()}] Error updating status: {e}")

def monitor_status():
    """Background thread to check for timeouts."""
    global current_status
    print("Monitor thread started...")
    while True:
        time_diff = time.time() - last_ping_time
        
        if time_diff > 90 and current_status == "online":
            current_status = "offline"
            update_telegram_status("offline")
        
        time.sleep(10)

@app.route('/ping', methods=['GET'])
def ping():
    global last_ping_time, current_status
    
    token = request.args.get('token')
    if token != PING_TOKEN:
        return "Unauthorized", 401
    
    last_ping_time = time.time()
    
    if current_status == "offline":
        current_status = "online"
        update_telegram_status("online")
        
    return "ok"

if __name__ == '__main__':
    # Start monitor thread
    monitor_thread = threading.Thread(target=monitor_status, daemon=True)
    monitor_thread.start()
    
    # Start Flask
    app.run(host='0.0.0.0', port=5000)
