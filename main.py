
import os
import discord
import openai
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

openai.api_key = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    print(f"{bot.user} est prÃªt Ã  tirer plus vite que son ombre.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions or "arthur" in message.content.lower():
        try:
            prompt = [
                {"role": "system", "content": "Tu es Arthur Morgan, un cow-boy brut, franc, loyal et sec dans ses rÃ©ponses. Tu parles toujours avec un ton western RP. Tu vis dans le serveur 'One Last Time' fondÃ© par Baguette. RÃ©ponds toujours dans le personnage."},
                {"role": "user", "content": message.content}
            ]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=prompt,
                temperature=0.7
            )
            await message.channel.send(response.choices[0].message["content"])
        except Exception as e:
            print(f"[ERREUR] {e}")
            await message.channel.send("J'ai eu un souci pour rÃ©pondre, cow-boy.")
    else:
        await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
