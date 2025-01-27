from telethon.tl.types import InputPeerUser
from utils import generate_report
recipients = [
    {"id": 2126443079, "access_hash": -765643097284794389},  # Replace with actual user IDs and access hashes   
]
async def send_broadcast(client, message):

    for recipient in recipients:
        user = InputPeerUser(recipient["id"], recipient["access_hash"])
        await client.send_message(user, message)
    # generate_report(recipients)