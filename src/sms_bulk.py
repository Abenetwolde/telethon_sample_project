
import os
import sys
import random
import time
import pickle
from pymongo import MongoClient
from telethon import Button, TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError, PeerFloodError,SessionPasswordNeededError
from telethon.tl.types import InputPeerUser
from telethon.sync import events
import pyfiglet

# Constants for console colors
light_green = '\033[92m'
white = '\033[0m'
red = '\033[91m'
cyan = '\033[96m'
rs = '\033[0m'


info = light_green + '(' + white + 'i' + light_green + ')' + rs
error = light_green + '(' + red + '!' + light_green + ')' + rs
success = white + '(' + light_green + '+' + white + ')' + rs
INPUT = light_green + '(' + cyan + '~' + light_green + ')' + rs
colors = [light_green, white, red, cyan]
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "telegram_bot"

try:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client[DB_NAME]
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    sys.exit()
# Constants for sleep time between messages (in seconds)
SLEEP_TIME = 20

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def banner_text():
    f = pyfiglet.Figlet(font='slant')
    banner = f.renderText('Telegram Bot')
    print(random.choice([light_green, white, red]) + banner + rs)

clear()
banner_text()
print(f'  Author: {white}Shamim Khaled{rs}\n')

accounts = [
    (21090672, "26502c28191d40af46f217af4e07a15d", "+251995004548"),

]

print(f'{INPUT}{light_green}({cyan}~{light_green}) Choose an account\n')
for i, acc in enumerate(accounts):
    print(f'{light_green}({white}{i}{light_green}) {acc[2]}')

ind = int(input(f'\n {INPUT}{light_green}({cyan}~{light_green}) Enter your choice: '))
api_id = accounts[ind][0]
api_hash = accounts[ind][1]
phone = accounts[ind][2]
 
c = TelegramClient(f'sessions\\{phone}', api_id, api_hash)
c.connect()

if not c.is_user_authorized():
    try:
        c.send_code_request(phone)
        code = input(f'{light_green}({cyan}~{light_green}) Enter the login code for {white}{phone}{red}: ')
        c.sign_in(phone, code)
    except SessionPasswordNeededError:
            password = input(f'{light_green}({cyan}~{light_green}) Enter your Telegram password: ')
            c.sign_in(password=password)
    except PhoneNumberBannedError:
        print(f'{error}{white}{phone}{red} is banned!{rs}')
        print(f'{error}{light_green} Run {white}manage.py{light_green} to filter them{rs}')
        sys.exit()
latest_message =  db.user_data.find_one({}, sort=[("_id", -1)])
print("user data............",latest_message)
if not latest_message:
    print("⚠️ No message found in the database. Exiting.")
    sys.exit()

message_text = latest_message.get("name", "")
media_path = latest_message.get("media_path", None)
button_link = latest_message.get("link", None)

buttons = [[Button.url("Click Here", button_link)]] if button_link else None
print("b`utton link............",buttons)

# Assuming members.csv file structure: username,user_id,access_hash,group,group_id,status
input_file = "members.txt"

users = [] 
with open(input_file, encoding='UTF-8') as f:
    lines = f.readlines()
    for line in lines[1:]:  # Skip the header line
        row = line.strip().split(',')
        print(row)
        if len(row) < 6:  # Ensure the row has all required fields
            print(f"Skipping malformed line: {line.strip()}")
            continue

    try:
            user = {
                'username': row[0].strip(),
                'user id': int(row[1].strip()),
                'access hash': int(row[2].strip()),
                'group': row[3].strip(),
                'group_id': row[4].strip(),
                'status': row[5].strip()
            }
            users.append(user)
    except ValueError as e:
            print(f"Skipping invalid line due to error: {e}")

print(f'{light_green}[1] Send SMS by user ID\n[2] Send SMS by username ')
mode = int(input(f'{light_green}Input: {rs}'))

# message = input(f'{light_green}[+] Enter Your Message: {rs}')

for user in users:
    try:
        if mode == 2:
            if user['username'] == "":
                continue
            receiver = c.get_input_entity(user['username'])
        elif mode == 1:
            receiver = InputPeerUser(user["user id"], user["access hash"])

            print(f"📤 Sending message to: {user['username']}")
            sent_message=None
            if media_path:
            # Step 1: Send media (without buttons) and store the message ID
             sent_message = c.send_file(receiver, media_path, caption=message_text)

            # Step 2: Edit the message to add buttons (only if buttons exist)
            if buttons and sent_message:
                c.send_message(receiver,  message_text, buttons=buttons)
            else:
            # Send text with buttons
             c.send_message(receiver, message_text, buttons=buttons)

            print(f"✅ Message sent to {user['username']}. Waiting {SLEEP_TIME} seconds...")
            time.sleep(SLEEP_TIME)
            
            # receiver = InputPeerUser(user['user id'], user['access hash'])
        else:
            print(f'{red}[!] Invalid Mode. Exiting.')
            c.disconnect()
            sys.exit()

        print(f'{light_green}[+] Sending Message to: {user["username"]}')
        # c.send_message(receiver, message.format(user['username']))
        print(f'{light_green}[+] Waiting {SLEEP_TIME} seconds')
        time.sleep(SLEEP_TIME)
    except PeerFloodError:
        print(f'{red}[!] Getting Flood Error from Telegram.')
        print(f'{red}[!] Script is stopping now. Please try again after some time.')
        c.disconnect()
        sys.exit()
    except Exception as e:
        print(f'{red}[!] Error: {e}')
        print(f'{red}[!] Trying to continue...')
        continue

c.disconnect()
print("Done. Message sent to all users.")
