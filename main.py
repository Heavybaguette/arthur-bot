import discord
import openai
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Important

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} est prêt à tirer plus vite que son ombre.")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    content_lower = message.content.lower()

    # Si le message contient "arthur"
    if "arthur" in content_lower:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Tu es Arthur Morgan, un cow-boy rustre mais loyal du Far West. Tu parles avec un ton direct, parfois un peu bourru, mais tu restes attachant."
                    },
                    {
                        "role": "user",
                        "content": message.content
                    }
                ]
            )

            reply = response.choices[0].message.content.strip()
            await message.channel.send(reply)

        except Exception as e:
            await message.channel.send("J'ai eu un souci pour répondre, cow-boy.")
            print("[ERREUR]", e)

client.run(TOKEN)
