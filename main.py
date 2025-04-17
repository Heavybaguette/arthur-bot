import discord
import os
import openai
import re
from discord.ext import commands
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} est prêt à tirer plus vite que son ombre.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content_lower = message.content.lower()
    author_name = message.author.display_name

    # Déclencheurs souples (nom + intention)
    trigger_detected = (
        "arthur" in content_lower or
        re.search(r"\b@?arthur morgan\b", content_lower)
    )

    intent_detected = any(keyword in content_lower for keyword in ["t'es là", "tu es là", "t'es dispo", "tu m'entends", "réponds", "?"])

    if trigger_detected and intent_detected:
        try:
            prompt = f"Tu es Arthur Morgan, un cow-boy rustre mais loyal. Tu réponds toujours de façon directe, sèche et dans un style western. Voici ce que {author_name} vient de dire : {message.content}"

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "Tu es Arthur Morgan de Red Dead Redemption 2."},
                          {"role": "user", "content": prompt}]
            )

            reply = response.choices[0].message.content
            await message.channel.send(reply)

        except Exception as e:
            print("[ERREUR]", e)
            await message.channel.send("J'ai eu un problème pour répondre, cow-boy.")

bot.run(DISCORD_TOKEN)
