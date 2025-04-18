import os
import discord
from discord.ext import commands
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client = discord.Client(intents=discord.Intents.all())
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ARTHUR_NAME = "Arthur Morgan"

def is_message_for_arthur(message):
    # S'adresse Ã  Arthur si : contient "arthur" OU rÃ©ponse directe Ã  Arthur
    if "arthur" in message.content.lower():
        return True
    if message.reference:
        try:
            replied_message = message.channel.fetch_message(message.reference.message_id)
            return replied_message.author.name == ARTHUR_NAME
        except:
            return False
    return False

@client.event
async def on_ready():
    print(f"{client.user} est prÃªt Ã  tirer plus vite que son ombre.")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if not is_message_for_arthur(message):
        return

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Tu es Arthur Morgan de Red Dead Redemption 2. Tu parles comme un cowboy, avec un ton sec et rustique, mais tu peux discuter de tout."
                },
                {
                    "role": "user",
                    "content": message.content
                }
            ]
        )
        await message.channel.send(response.choices[0].message.content)
    except Exception as e:
        await message.channel.send("J'ai eu un souci pour rÃ©pondre, cow-boy.")
        print(f"[ERREUR] {e}")

client.run(TOKEN)
