# from asyncio import subprocess
import subprocess
from telethon import Button, TelegramClient, events
from pymongo import MongoClient
# Replace with your API credentials
api_id = '21090672'
api_hash = '26502c28191d40af46f217af4e07a15d'
bot_token = '7756739063:AAECItLDb84LY5Ai0C1kmdM8I55810jXQ2s'
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "telegram_bot"
COLLECTION_NAME = "user_data"
bot = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]
try:
    mongo_client = MongoClient(MONGO_URI)
    mongo_client.admin.command("ping")  # Test connection
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    chat = event.chat_id

    async with bot.conversation(chat) as conv:
        # Step 1: Ask for the user's name
        await conv.send_message("👋 Hi! What's your name?")
        name = await conv.get_response()

   

        # Step 3: Ask for media upload (with "Skip" button)
        media_message = await conv.send_message(
            "📸 Please upload a **photo, GIF, or video**, or press **Skip**.",
            buttons=[Button.text("Skip ✅", resize=True)]
        )

        media = await conv.get_response()
        media_path = None

        # Step 4: Handle user response
        if media.text.lower() == "skip ✅":
            media = None  # No media uploaded
        elif media.media:
            media_path = await bot.download_media(media, file=f"{chat}_media")

        # Step 5: Ensure that the media message exists before trying to edit it
        try:
            if media_message:  # Check if the media message was successfully sent
                await bot.edit_message(chat,"✅ Media selection completed!")
        except Exception as e:
            print(f"Error editing message: {e}")

        # Step 6: Ask for the link to add to the inline button
        await conv.send_message("🔗 Please provide the link you want to be added to the inline button.")
        link_message = await conv.get_response()

        # Step 7: Prepare the final message
        caption = f"👤 **Name:** {name.text}\n🎂"
        buttons = [[Button.url("Click Here", link_message.text)]]
        
        if media_path:
            message = await bot.send_file(chat, media_path, caption=caption, buttons=buttons)
        else:
            message = await conv.send_message(caption, buttons=buttons)
        # Save user data to MongoDB
        user_data = {
            "chat_id": chat,
            "name": name.text,
            "media_path": media_path,
            "link": link_message.text,
            "message_id": message.id
        }
        collection.insert_one(user_data)
            # Step 9: Send separate message with broadcast button (to avoid mixed inline + normal button error)
        await conv.send_message("📢 Click below to broadcast this message:", buttons=Button.text("📢 Broadcast", resize=True))
        # bot.final_message = message
@bot.on(events.NewMessage(pattern="📢 Broadcast"))
async def broadcast(event):
    sender = await event.get_sender()
    

    # final_message = bot.final_message

    # if not final_message:
    #     await event.reply("⚠️ No message to broadcast.")
    #     return

    # Run the external broadcast script
    try:
        subprocess.run(["python", "sms_bulk.py"], check=True)
        await event.reply("✅ Broadcast started!")
    except Exception as e:
        await event.reply(f"❌ Error: {e}")



# Start the bot
print("🤖 Bot is running...")
bot.run_until_disconnected()
 