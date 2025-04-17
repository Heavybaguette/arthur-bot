import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

client = OpenAI(api_key=OPENAI_API_KEY)

@bot.event
async def on_ready():
    print(f"{bot.user} est prÃªt Ã  tirer plus vite que son ombre.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()
    if "arthur" in content or bot.user.mentioned_in(message):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": (
                        "Tu es Arthur Morgan, un cow-boy franc, brut, loyal. "
                        "Tu parles toujours en franÃ§ais dans un style RP western sec et direct. "
                        "Tu fais partie du serveur One Last Time, fondÃ© par Baguette. "
                        "Pour rejoindre le serveur, on utilise F8 puis : connect 88.198.53.38:30075."
                    )},
                    {"role": "user", "content": message.content}
                ]
            )
            reply = response.choices[0].message.content
            await message.channel.send(reply)
        except Exception as e:
            print(f"[ERREUR] {e}")
            await message.channel.send("J'ai eu un souci pour rÃ©pondre, cow-boy.")

bot.run(DISCORD_TOKEN)
