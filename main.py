
import discord
import openai
import os
import random

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

openai.api_key = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

cowboy_replies = [
    "Ouais, j’suis là cow-boy. Parle vite ou dégaine avant que j’me lasse.",
    "Toujours prêt à dégainer une réponse... qu’est-ce qu’il te faut ?",
    "J’suis pas un moulin à paroles, mais vas-y, j’t’écoute.",
    "Ça parle, ça parle... mais est-ce que t’as quelque chose d’important à dire ?",
    "Hmm... j’me demande si t’es pas en train de gaspiller mon temps.",
    "Ouais. C’est moi. Arthur. Maintenant, fais court, cow-boy.",
    "J’ai les bottes dans la boue et les nerfs à vif. T’as intérêt à aller droit au but."
]

@client.event
async def on_ready():
    print(f"{client.user} est prêt à tirer plus vite que son ombre.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.lower()

    if "arthur" in content or client.user.mention in message.content:
        try:
            if "comment on rejoint le serv" in content:
                await message.channel.send("Tu veux mettre les pieds dans One Last Time, hein ? Tape `F8` et colle ça : `connect 88.198.53.38:30075`. Bienvenue dans l’Ouest, partenaire.")
                return

            prompt = f"Réponds comme un cow-boy nommé Arthur Morgan dans le style de Red Dead Redemption 2. Sois sec, direct et un peu rustre. Voici ce qu’on t’a dit : {message.content}"

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Tu es Arthur Morgan, un cow-boy rustre et direct, membre de la bande de Dutch dans Red Dead Redemption 2."},
                    {"role": "user", "content": prompt}
                ]
            )

            await message.channel.send(response.choices[0].message.content)

        except Exception as e:
            print("[ERREUR]", e)
            await message.channel.send(random.choice(cowboy_replies))
