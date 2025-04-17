import discord
import openai
import os
import random
import asyncio
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
openai.api_key = os.getenv("OPENAI_API_KEY")

cowboy_phrases = [
    "Hmm... laisse-moi réfléchir...",
    "Attends un peu, cow-boy...",
    "Minute, j’essaie de piger ton histoire...",
]

@client.event
async def on_ready():
    print(f'{client.user} est prêt à tirer plus vite que son ombre.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    contenu = message.content.lower()

    # ⚡ Détection intelligente : Arthur + un verbe ou une question
    if "arthur" in contenu:
        try:
            prompt = (
                f"Tu es Arthur Morgan dans Red Dead Redemption 2. Tu réponds comme un cowboy, avec un ton sec et direct. "
                f"Le serveur s'appelle One Last Time et pour se connecter il faut faire F8 puis connect 88.198.53.38:30075. "
                f"Ton créateur s'appelle Baguette. Voici ce qu'on t'a dit : \"{message.content}\""
            )

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.8
            )

            reply = response.choices[0].message.content.strip()
            await message.channel.send(reply)

        except Exception as e:
            print(f"[ERREUR] {e}")
            await message.channel.send(random.choice(cowboy_phrases) + "\nJ'ai eu un problème pour répondre, cow-boy.")

client.run(os.getenv("DISCORD_TOKEN"))
