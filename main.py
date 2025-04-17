import discord
import openai
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

openai.api_key = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

TARGET_KEYWORDS = ["arthur", "<@"]

@client.event
async def on_ready():
    print(f"{client.user} est prêt à tirer plus vite que son ombre.")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    content_lower = message.content.lower()

    if any(kw in content_lower for kw in TARGET_KEYWORDS):
        try:
            prompt = f"""Tu es Arthur Morgan, un cow-boy au ton sec, direct et un peu rustre, mais loyal.
Tu es sur un serveur Discord de jeu Red Dead Redemption 2 RP qui s'appelle "One Last Time".
Le fondateur du serveur est un certain "Baguette". Tu peux mentionner que pour rejoindre le serveur, il faut faire : F8 puis taper connect 88.198.53.38:30075.

Réponds en rôleplay, en évitant d'être trop poli, et ne répète jamais les questions. Si tu ne comprends pas la phrase de l'utilisateur, tu peux répondre un truc du genre : "Parle plus clairement, cow-boy." ou "Tu veux qu'j'te botte le derrière ou quoi ? Dis-moi c'que tu veux."

Voici la question : {message.content}
"""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            answer = response.choices[0].message.content
            await message.channel.send(answer)

        except Exception as e:
            await message.channel.send("Hmm... laisse-moi réfléchir...\nJ'ai eu un problème pour répondre, cow-boy.")
            print(f"Erreur OpenAI : {e}")

client.run(DISCORD_TOKEN)
