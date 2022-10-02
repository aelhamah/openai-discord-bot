import os
import discord
import openai
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

context = ""

@client.event
async def on_message(message):
    global context
    if message.author == client.user or message.channel is None:
        return

    # Clear prompt context manually (or automatically if context gets too long)
    if '#new context' in message.content or len(context) > 1000:
        context = ""
        await message.channel.send("Context cleared")
        
    if '#new context' in message.content:
        return

    openai.api_key = os.getenv("OPENAI_API_KEY")
    context += f"Person 1: {message.content}\nPerson 2:"
    response = openai.Completion.create(model="text-davinci-002", prompt=context, temperature=0.2, max_tokens=20)
    context += f" {response.choices[0].text}\n"
    await message.channel.send(response.choices[0].text)


client.run(TOKEN)