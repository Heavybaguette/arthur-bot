import discord
import openai
import os
from sentence_transformers import SentenceTransformer, util

# Clés d’API
TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Intents Discord
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

# Modèle NLP pour comprendre le sens des phrases
model = SentenceTransformer("all-MiniLM-L6-v2")

# Intentions prévues + réponses à la Arthur
intents_list = {
    "comment rejoindre le serveur": "Pour rejoindre One Last Time, tape F8 puis : connect 88.198.53.38:30075",
    "adresse du serveur": "Voici l'adresse directe du saloon numérique : connect 88.198.53.38:30075",
    "où est le serveur": "Faut taper ça dans ta console cow-boy : connect 88.198.53.38:30075",
    "serveur one last time": "One Last Time, c’est F8 puis : connect 88.198.53.38:30075. N’oublie pas ton chapeau.",
}

@client.event
async def on_ready():
    print(f"{client.user} est prêt à dégainer plus vite que son ombre.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_input = message.content.lower()

    # Si le message contient "arthur", le bot se sent concerné
    if "arthur" in user_input:
        input_embedding = model.encode(user_input, convert_to_tensor=True)

        best_score = 0
        best_response = None

        for intent, response in intents_list.items():
            intent_embedding = model.encode(intent, convert_to_tensor=True)
            score = util.pytorch_cos_sim(input_embedding, intent_embedding).item()

            if score > best_score:
                best_score = score
                best_response = response

        if best_score > 0.6:
            await message.channel.send(best_response)
        else:
            await message.channel.send("Hmm… j’suis pas certain d’comprendre c’que tu veux dire, partenaire.")
