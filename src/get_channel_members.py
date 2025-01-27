from telethon.tl.types import ChannelParticipantsSearch
from telethon.errors.rpcerrorlist import ChannelPrivateError

async def scrape_channel_members(client, channel_identifier, output_file="channel_members.txt"):
    try:
        # Get the channel entity
        if channel_identifier.startswith("-100"):  # Check if it's a numeric ID
            channel_identifier = int(channel_identifier)

        # Get the channel entity
        channel = await client.get_entity(channel_identifier)
        print(f"Scraping members from channel: {channel.title}")

        # Fetch participants
        members = await client.get_participants(channel)  # Fetch all members
        print(f"Found {len(members)} members in the channel.")

        # Save members to a text file
        with open(output_file, mode='w', encoding='utf-8') as file:
            file.write("User ID | Access Hash | Username | First Name | Last Name\n")
            file.write("=" * 80 + "\n")

            for member in members:
                line = f"{member.id} | {member.access_hash} | {member.username or 'N/A'} | {member.first_name or 'N/A'} | {member.last_name or 'N/A'}\n"
                file.write(line)

        return f"Successfully saved {len(members)} members to {output_file}."
    except ChannelPrivateError:
        return "Failed to access the channel. Make sure the bot is a member of the channel."
    except Exception as e:
        return f"An error occurred: {e}"
