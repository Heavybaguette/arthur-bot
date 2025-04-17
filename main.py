import os
import discord
from discord.ext import commands
from openai import OpenAI

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Client OpenAI (version >= 1.0.0)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@bot.event
async def on_ready():
    print(f"{bot.user} est prêt à tirer plus vite que son ombre.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Tu es Arthur Morgan. Réponds comme un cow-boy du Far West, avec du caractère, mais reste amical."},
                    {"role": "user", "content": message.content}
                ]
            )

            reply = response.choices[0].message.content
            await message.channel.send(reply)

        except Exception as e:
            await message.channel.send("Hmm... laisse-moi réfléchir...\nJ'ai eu un problème pour répondre, cow-boy.")
            print(f"Erreur OpenAI : {e}")

bot.run(os.getenv("DISCORD_TOKEN"))
