
import discord
from discord.ext import commands
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@bot.event
async def on_ready():
    print(f"{bot.user} est prÃªt Ã  tirer plus vite que son ombre.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()
    if "arthur" in content:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Tu es Arthur Morgan de Red Dead Redemption 2. Tu parles comme un cow-boy, de maniÃ¨re un peu brute mais polie, avec un style RP en franÃ§ais."
                    },
                    {
                        "role": "user",
                        "content": message.content
                    }
                ]
            )
            await message.channel.send(response.choices[0].message.content)
        except Exception as e:
            print(f"Erreur : {e}")
            await message.channel.send("J'ai eu un souci pour rÃ©pondre, cow-boy.")
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
