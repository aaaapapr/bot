# This example requires the 'message_content' intent.
import discord
import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")


def get_quote():
  response = requests.get("http://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote


def get_joke():
  response = requests.get("https://v2.jokeapi.dev/joke/Any")
  json_data = json.loads(response.text)
  joke = json_data['setup'] + ".........." + json_data['delivery']
  return joke


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):

  if message.author == client.user:
    return

  if message.content.startswith('!help'):
    await message.channel.send(
        '!hello - Say hello to the bot\n!inspire - Get an inspirational quote\n!help - Get help with the bot\n!joke - Get a joke'
    )

  if message.content.startswith('!hello'):
    await message.channel.send('Hello!')

  if message.content.startswith('!inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if message.content.startswith("!joke"):
    try:
      joke = get_joke()
      await message.channel.send(joke)
    except:
      print("error")

client.run(token)
