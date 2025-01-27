from telethon import TelegramClient, events
from config import api_id, api_hash, bot_token
from handlers import handle_send_command, handle_user_responses
from get_channel_members import scrape_channel_members

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
async def get_user_info(client, username):
    try:
        # Retrieve the entity (user) using a username or user ID
        user = await client.get_entity(username)  # You can use a username, user ID, or phone number
        user_id = user.id
        access_hash = user.access_hash
        
        print(f"User ID: {user_id}")
        print(f"Access Hash: {access_hash}")
        
        return user_id, access_hash
    except Exception as e:
        print(f"Error: {e}")
        return None, None

# Register event handlers
@client.on(events.NewMessage(pattern='/send'))
async def send_handler(event):
    username = 'zzzzzvff'  # Replace with the actual username or user ID
    user_id, access_hash = await get_user_info(client, username)
    await handle_send_command(event, client)

@client.on(events.NewMessage())  # Event to handle user responses
async def handle_user_converstion(event):
    if event.text.startswith("/send"):
        return
    await handle_user_responses(event)
@client.on(events.NewMessage(pattern='/scrapemembers'))
async def scrape_members_handler(event):
    try:
        # Extract channel username or ID from the message
        command_args = event.text.split()
        if len(command_args) < 2:
            await event.respond("Please specify the channel username or ID: `/scrapemembers <channel_username>`")
            return

        channel_username = command_args[1]  # Get channel username from the command
        output_file = "channel_members.txt"  # Default output file

        # Call the scrape function
        status_message = await scrape_channel_members(client, channel_username, output_file)

        # Respond to the user
        await event.respond(status_message)
    except Exception as e:
        await event.respond(f"An error occurred: {e}")
# Run the bot
client.run_until_disconnected()
