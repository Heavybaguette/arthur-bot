import discord
import openai
import os

intents = discord.Intents.default()
intents.message_content = True
intents.presences = False
intents.members = False

client = discord.Client(intents=intents)

openai.api_key = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

@client.event
async def on_ready():
    print(f"{client.user} est prêt à tirer plus vite que son ombre.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions or "arthur" in message.content.lower():
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Tu es Arthur Morgan, un cowboy bourru mais loyal, parlant avec un ton western."},
                    {"role": "user", "content": message.content}
                ]
            )
            await message.channel.send(response.choices[0].message.content)
        except Exception as e:
            await message.channel.send(f"Erreur OpenAI : {str(e)}")

client.run(DISCORD_TOKEN)
