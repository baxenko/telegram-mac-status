from pyrogram import Client
from dotenv import load_dotenv
import os

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

if not API_ID:
    print("Please fill .env file first")
    exit()

app = Client("session", api_id=API_ID, api_hash=API_HASH)

print("Logging in...")
with app:
    me = app.get_me()
    print(f"Success! Logged in as: {me.first_name}")
    print("Session file created.")
