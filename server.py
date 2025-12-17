import os
import time
import threading
from datetime import datetime
from flask import Flask, request
from pyrogram import Client
from dotenv import load_dotenv

# Load config
load_dotenv()

app = Flask(__name__)

# Config
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PING_TOKEN = os.getenv("PING_TOKEN")
ONLINE_EMOJI = os.getenv("ONLINE_EMOJI", "🟢")
OFFLINE_EMOJI = os.getenv("OFFLINE_EMOJI", "🔴")

last_ping_time = time.time()
current_status = "online"

client = Client("session", api_id=API_ID, api_hash=API_HASH)

def update_telegram_profile(status_emoji):
    try:
        with client:
            client.update_profile(last_name=status_emoji)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Updated: {status_emoji}")
    except Exception as e:
        print(f"Error: {e}")

def monitor_loop():
    global current_status
    while True:
        time.sleep(10)
        if time.time() - last_ping_time > 90 and current_status == "online":
            current_status = "offline"
            update_telegram_profile(OFFLINE_EMOJI)

@app.route('/ping', methods=['GET'])
def ping_handler():
    global last_ping_time, current_status
    if request.args.get('token') != PING_TOKEN:
        return "Forbidden", 403
    
    last_ping_time = time.time()
    
    if current_status == "offline":
        current_status = "online"
        update_telegram_profile(ONLINE_EMOJI)
        
    return "pong"

if __name__ == '__main__':
    threading.Thread(target=monitor_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=5050)
