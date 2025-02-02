import os
import sys
import time
import asyncio
import random
import pyfiglet
from telethon import Button, TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors.rpcerrorlist import PhoneNumberBannedError, PeerFloodError, SessionPasswordNeededError
from telethon.tl.types import InputPeerUser

# Telegram API credentials (Replace with your values)
api_id = '21090672'
api_hash = '26502c28191d40af46f217af4e07a15d'
bot_token = '7756739063:AAECItLDb84LY5Ai0C1kmdM8I55810jXQ2s'
phone = "+251995004548"  # Replace with your phone number
input_file = "members.txt"
# Target channel (Replace with your channel username or ID)
channel_username = "asddddddddddddds"
client = TelegramClient(f'sessions/{phone}', api_id, api_hash)
# Initialize Telegram client
SLEEP_TIME = 30
async def main():
    await client.connect()

    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone)
            code = input("Enter the login code: ")
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            password = input("Enter your Telegram password: ")
            await client.sign_in(password=password)
        except PhoneNumberBannedError:
            print(f"❌ {phone} is banned!")
            sys.exit()

    # Read members from file
    users = []
    with open(input_file, encoding='UTF-8') as f:
        lines = f.readlines()
        for line in lines[1:]:  # Skip header
            row = line.strip().split(',')
            if len(row) < 6:
                print(f"Skipping malformed line: {line.strip()}")
                continue
            try:
                user = {
                    'username': row[0].strip(),
                    'user_id': int(row[1].strip()),
                    'access_hash': int(row[2].strip()),
                }
                users.append(user)
            except ValueError as e:
                print(f"Skipping invalid line: {e}")

    # Get channel entity
    try:
        channel = await client.get_entity(channel_username)
    except Exception as e:
        print(f"Error fetching channel: {e}")
        sys.exit()

    # Add members to channel
    for user in users:
        try:
            peer = InputPeerUser(user["user_id"], user["access_hash"])
            await client(InviteToChannelRequest(channel, [peer]))  # Add user to channel
            print(f"✅ Added {user['username']} to {channel_username}")
            await asyncio.sleep(SLEEP_TIME)  # Prevent flood limits

        except PeerFloodError:
            print("🚨 Telegram is limiting the script. Try again later.")
            sys.exit()
        except Exception as e:
            print(f"❌ Error adding {user['username']}: {e}")

    await client.disconnect()
    print("🎉 Done! All members processed.")

# Run the async function
asyncio.run(main())