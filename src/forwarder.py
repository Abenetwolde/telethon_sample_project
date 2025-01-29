from telethon import TelegramClient, events

# Replace these with your Telegram API credentials
API_ID = '21090672'
API_HASH = '26502c28191d40af46f217af4e07a15d'
SESSION_NAME = 'forwarder'  # Name of your session file

# Replace with the source and target group/channel IDs or usernames
SOURCE_CHAT = '-1002296034146'  # e.g., '-1001234567890' or 'source_channel'
TARGET_CHAT = '-1002292710072'  # e.g., '-1009876543210' or 'target_channel'

# Initialize the Telegram client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def main():
    # Fetch the chat entities to ensure the bot can access them
    try:
        print("Fetching chat entities...")
        source_chat_SOURCE_CHAT = int(SOURCE_CHAT)
        source_chat = await client.get_entity(source_chat_SOURCE_CHAT)
        target_chatSOURCE_CHAT = int(TARGET_CHAT)
        target_chat = await client.get_entity(target_chatSOURCE_CHAT)
        print(f"Source chat: {source_chat.title}")
        print(f"Target chat: {target_chat.title}")
    except Exception as e:
        print(f"Failed to fetch chat entities: {e}")
        return

    # Event handler to monitor messages in the source chat
    @client.on(events.NewMessage(chats=source_chat))
    async def forward_message(event):
        try:
            # Forward or copy the message to the target chat
            # For forwarding (keeps original sender info):
            # await event.forward_to(target_chat)

            # For copying (appears as your bot's message):
            await client.send_message(
                target_chat,
                event.message.text or '',  # Message text
                file=event.message.media    # Forward media if present
            )
            print(f"Message forwarded to {target_chat.id}: {event.message.text}")
        except Exception as e:
            print(f"Failed to forward message: {e}")

    # Start the client
    print("Bot is running...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())