from telethon import events
from telethon.tl.types import InputPeerUser
from utils import generate_report
from broadcast import send_broadcast
from scheduler import schedule_message
import datetime

ADMIN_USER_IDS = [123456789, 987654321]  # Replace with actual admin user IDs

user_states = {}  # Dictionary to track user states

def is_admin(user_id):
    return user_id in ADMIN_USER_IDS

async def handle_send_command(event, client):
    sender = await event.get_sender()
    # if not is_admin(sender.id):
    #     await event.respond("You are not authorized to use this command.")
    #     return

    user_states[sender.id] = {"step": "awaiting_message"}
    if event.message.media:
        user_states[sender.id]["message"] = event.message
        user_states[sender.id]["step"] = "awaiting_schedule_choice"
        await event.respond(
            "Media detected. Should the message be sent immediately or scheduled for later? (Reply with 'immediately' or 'schedule')"
        )
    else:
        await event.respond("Please input the message and attach any media (optional).")
    print("user_states:", user_states)  # Debugging line to print the state

async def handle_user_responses(event):
    print("Received message:", event.text)  # Debugging line to print the incoming message
    sender = await event.get_sender()
    
    # Ensure the user is in a conversation flow
    if sender.id not in user_states:
        return  # Ignore messages from users who are not in a conversation flow

    state = user_states[sender.id]

    if state["step"] == "awaiting_message":
        # Save the user's message and move to the next step
        state["message"] = event.message
        state["step"] = "awaiting_schedule_choice"
        await event.respond(
            "Should the message be sent immediately or scheduled for later? (Reply with 'immediately' or 'schedule')"
        )
    elif state["step"] == "awaiting_schedule_choice":
        if event.text.lower() == "immediately":
            await send_broadcast(event.client, state["message"])
            del user_states[sender.id]
            await event.respond("Message sent successfully!")
        elif event.text.lower() == "schedule":
            state["step"] = "awaiting_schedule_time"
            await event.respond("Please specify the date and time (YYYY-MM-DD HH:MM).")
        else:
            await event.respond("Invalid option. Reply with 'immediately' or 'schedule'.")
    elif state["step"] == "awaiting_schedule_time":
        try:
            # Parse and schedule the message
            schedule_time = datetime.datetime.strptime(event.text, "%Y-%m-%d %H:%M")
            schedule_message(event.client, state["message"], schedule_time)
            del user_states[sender.id]
            await event.respond("Message scheduled successfully!")
        except ValueError:
            await event.respond("Invalid date and time format. Please try again.")

recipients = [
    {"id": 2126443079, "access_hash": -765643097284794389},  # Replace with actual user IDs and access hashes
   
]
 
async def send_broadcast(client, message):
    for recipient in recipients:
        user = InputPeerUser(recipient["id"], recipient["access_hash"])
        await client.send_message(user, message)
    # generate_report(recipients)
