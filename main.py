import os
import discord
from discord.ext import commands
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

@bot.event
async def on_ready():
    print(f"{bot.user} est prêt à tirer plus vite que son ombre.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()
    if "arthur" in content or bot.user.mentioned_in(message):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": (
                        "Tu es Arthur Morgan du jeu Red Dead Redemption 2. "
                        "Tu parles comme un cowboy, un peu brut mais loyal. "
                        "Tu réponds de manière RP, dans un ton sec et direct. "
                        "Le serveur s'appelle One Last Time, fondé par Baguette. "
                        "Pour rejoindre le serveur, il faut faire F8 > connect 88.198.53.38:30075."
                    )},
                    {"role": "user", "content": message.content}
                ]
            )

            reply = response.choices[0].message.content
            await message.channel.send(reply)

        except Exception as e:
            print(f"[ERREUR] {e}")
            await message.channel.send("J'ai eu un souci pour répondre, cow-boy.")

bot.run(os.getenv("DISCORD_TOKEN"))
