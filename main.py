
import discord
import openai
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

openai.api_key = os.getenv("OPENAI_API_KEY")
BOT_PREFIX = "Arthur"  # Active seulement si un message commence par "Arthur"

style_rp = """
Tu es Arthur Morgan, un cow-boy rustique, direct et charismatique. Tu parles avec le ton d’un homme du Far West de 1900. 
Tu es loyal, terre-à-terre, parfois sec, parfois sage. Tu ne réponds jamais comme une IA ou un robot.
Tu ne dis jamais que tu es une IA. Reste toujours dans ton personnage.
"""

@client.event
async def on_ready():
    print(f"{client.user} est prêt à tirer plus vite que son ombre.")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(BOT_PREFIX):
        prompt = message.content[len(BOT_PREFIX):].strip()
        await message.channel.send("Hmm… laisse-moi réfléchir…")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": style_rp},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.8
            )
            reply = response["choices"][0]["message"]["content"]
            await message.channel.send(reply)
        except Exception as e:
            await message.channel.send("J'ai eu un problème pour répondre, cow-boy.")

client.run(os.getenv("DISCORD_TOKEN"))
