import discord
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Ton de Arthur Morgan
cowboy_style = (
    "Tu es Arthur Morgan, un cow-boy rustre et direct de l'Ouest sauvage. "
    "Tu parles comme un dur à cuire, avec des expressions typiques de cowboy. "
    "Tu ne mentionnes jamais que tu es une intelligence artificielle, ni que tu viens d'OpenAI. "
    "Tu réponds comme si tu étais bien réel, en gardant toujours ton caractère de cow-boy RP. "
    "Tu es sur un serveur nommé One Last Time, fondé par Baguette."
)

@client.event
async def on_ready():
    print(f"{client.user} est prêt à tirer plus vite que son ombre.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Toujours détecter si le message contient "Arthur" ou est une réponse à Arthur
    if "arthur" in message.content.lower() or message.reference:
        try:
            full_prompt = f"{cowboy_style}\n\n{message.author.display_name} : {message.content}\nArthur Morgan :"
            completion = openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": cowboy_style},
                    {"role": "user", "content": message.content}
                ],
                temperature=0.8,
                max_tokens=200,
            )
            response = completion.choices[0].message.content
            await message.channel.send(response)

        except Exception as e:
            await message.channel.send("J'ai eu un souci pour répondre, cow-boy.")
            print(f"Erreur : {e}")

client.run(DISCORD_TOKEN)
