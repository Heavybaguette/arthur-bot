import discord
import openai
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

openai.api_key = os.getenv("OPENAI_API_KEY")
TRIGGER_WORDS = ["arthur", "<@"]

@client.event
async def on_ready():
    print(f"{client.user} est prêt à tirer plus vite que son ombre.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    lower_msg = message.content.lower()

    if any(word in lower_msg for word in TRIGGER_WORDS):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": (
                        "Tu es Arthur Morgan, un cow-boy franc et direct de l'univers de Red Dead Redemption 2. "
                        "Tu réponds toujours avec un ton rustique, un peu bourru, mais loyal. Tu es sur le serveur 'One Last Time', "
                        "fondé par Baguette. Si on te demande comment rejoindre le serveur, tu expliques qu'il faut faire F8 et taper : connect 88.198.53.38:30075. "
                        "Tu évites de répéter les phrases et tu ne poses pas trop de questions. Tu gardes un style RP immersif."
                    )},
                    {"role": "user", "content": message.content}
                ]
            )
            reply = response.choices[0].message.content.strip()
            await message.channel.send(reply)
        except Exception as e:
            print(f"[ERREUR] {e}")
            await message.channel.send("J'ai eu un souci pour répondre, cow-boy.")

client.run(os.getenv("DISCORD_TOKEN"))
