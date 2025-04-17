
import os
import discord
from discord.ext import commands
from discord import Intents
from openai import OpenAI

intents = Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

@bot.event
async def on_ready():
    print(f"{bot.user} est prÃªt Ã  tirer plus vite que son ombre.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message) or "arthur" in message.content.lower():
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Tu es Arthur Morgan, un cow-boy au franc parler. Tu rÃ©ponds en franÃ§ais, de maniÃ¨re brute et directe, avec un ton RP."},
                    {"role": "user", "content": message.content}
                ]
            )
            await message.channel.send(response.choices[0].message.content)
        except Exception as e:
            print("[ERREUR]", e)
            await message.channel.send("J'ai eu un souci pour rÃ©pondre, cow-boy.")

bot.run(os.getenv("DISCORD_TOKEN"))
