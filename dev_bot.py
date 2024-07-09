# This example requires the 'message_content' intent.
import discord
import requests
import json
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


@st.experimental_fragment
def run_bot():

    token = os.getenv("TOKEN")

    def get_quote():
        response = requests.get("http://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]["q"] + " -" + json_data[0]["a"]
        return quote

    def get_joke():
        response = requests.get("https://v2.jokeapi.dev/joke/Any")
        json_data = json.loads(response.text)
        joke = json_data["setup"] + ".........." + json_data["delivery"]
        return joke

    def get_bitcoin_price():
        response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
        json_data = json.loads(response.text)
        bitcoin_price = json_data["bpi"]["USD"]["rate_float"]
        return bitcoin_price
    
    def  get_meaning(word):
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        json_data = json.loads(response.text)
        return json_data

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"We have logged in as {client.user}")

    @client.event
    async def on_message(message):

        if message.author == client.user:
            return

        if message.content.startswith("!help"):
            await message.channel.send(
                "!hello - Say hello to the bot\n!inspire - Get an inspirational quote\n!help - Get help with the bot\n!joke - Get a joke\n!bitcoin - Get current bitcoin price\n!def AnyWord - get the definition of the word"
            )

        if message.content.startswith("!hello"):
            await message.channel.send("Hello!")

        if message.content.startswith("!inspire"):
            quote = get_quote()
            await message.channel.send(quote)

        if message.content.startswith("!joke"):
            try:
                joke = get_joke()
                await message.channel.send(joke)
            except:
                print("error")
        if message.content.startswith("!bitcoin"):
            try:
                bitcoin_price = get_bitcoin_price()
                await message.channel.send(f"Current bitcoin price - {bitcoin_price}")
            except:
                print("error")
        
        if message.content.startswith("!def"):
            try:
                print(message.content.split()[1])
                if(message.content.split()[1]):
                    word = message.content.split()[1]
                    json_data = get_meaning(word)
                    for meaning in json_data[0]["meanings"]:
                        final_string = f"Part of Speech: {meaning["partOfSpeech"]}\nDefinition: {meaning["definitions"][0]["definition"]}\n"
                        await message.channel.send(f"{final_string} ----------------------------------------------------------------- \n" )
                else:
                    await message.channel.send("Sorry I did not recieve a word☹️")
            except:
                print("error")

    client.run(token)


st.title("Discord Bot!!")
run_bot()
