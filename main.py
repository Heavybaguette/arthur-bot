import discord
import openai
import os
from sentence_transformers import SentenceTransformer, util

TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

# 🔎 Modèle pour compréhension du langage
model = SentenceTransformer("all-MiniLM-L6-v2")

# 🌵 Liste d’intentions reconnues avec réponses western
intents_list = {
    "comment rejoindre le serveur": "Pour rejoindre One Last Time, ouvre F8 et tape : connect 88.198.53.38:30075",
    "quelle est l'adresse du serveur": "Saisis bien ça dans ta console cow-boy : connect 88.198.53.38:30075",
    "serveur": "Si tu parles du serveur RP, tape F8 et écris : connect 88.198.53.38:30075, étranger.",
}

@client.event
async def on_ready():
    print(f"{client.user} est prêt à tirer plus vite que son ombre.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_input = message.content.lower()
    
    # Embedding de l'entrée utilisateur
    input_embedding = model.encode(user_input, convert_to_tensor=True)

    best_score = 0
    best_response = None

    for intent, reply in intents_list.items():
        intent_embedding = model.encode(intent, convert_to_tensor=True)
        score = util.pytorch_cos_sim(input_embedding, intent_embedding).item()

        if score > best_score:
            best_score = score
            best_response = reply

    # Seuil de déclenchement
    if best_score > 0.6:
        await message.channel.send(best_response)
    elif "arthur" in user_input:
        await message.channel.send("Hmm... laisse-moi réfléchir...\nJ'ai eu un problème pour répondre, cow-boy.")

client.run(TOKEN)
