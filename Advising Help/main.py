from typing import Final
import sys
sys.stdout.reconfigure(encoding='utf-8')
from discord import Intents, Client, Message
import os
from dotenv import load_dotenv
from responses import fetch_course_data

load_dotenv()

TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

@client.event
async def on_ready() -> None:
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    if message.content.startswith('/course'):
        keyword = message.content[len('/course '):].strip().upper()
        if not keyword:
            await message.channel.send("Please provide a course keyword. Format: /course <course_code>")
            return
        try:
            course_messages = fetch_course_data(keyword)
            for msg in course_messages:
                await message.channel.send(msg)
        except Exception as e:
            await message.channel.send(f"An error occurred: {e}")

def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()