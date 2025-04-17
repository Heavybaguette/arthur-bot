
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import openai

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

openai.api_key = OPENAI_API_KEY

@bot.event
async def on_ready():
    print(f"{bot.user} est prêt à tirer plus vite que son ombre.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()

    # Détection flexible avec quelques mots-clés et contexte global
    keywords = ["arthur", "arthur morgan", "<@"]
    if any(keyword in content for keyword in keywords):
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Tu es Arthur Morgan, un cowboy rustre et direct, membre du gang de Dutch dans Red Dead Redemption 2. Tu réponds toujours avec un ton sec, brut, mais poli à ceux qui t’interpellent dans un serveur Discord RP nommé 'One Last Time'. Le fondateur du serveur s'appelle Baguette. Quand quelqu’un te demande comment rejoindre le serveur, tu dois répondre en expliquant qu’il faut lancer F8 dans RedM et taper : connect 88.198.53.38:30075"},
                    {"role": "user", "content": content}
                ]
            )
            reply = response.choices[0].message.content.strip()
            await message.channel.send(reply)

        except Exception as e:
            await message.channel.send(f"Attends un peu, cow-boy...\nJ'ai eu un problème pour répondre, cow-boy.")
            print(f"[ERREUR OPENAI] {e}")

bot.run(DISCORD_TOKEN)
