# This example requires the 'message_content' intent.

import discord
import requests
from bs4 import BeautifulSoup
import re
import os

# Define the target URL
uscf_url = "https://www.uschess.org/msa/thin.php"


intents = discord.Intents(messages=True, guilds=True)
intents.members=True
intents.message_content=True

client = discord.Client(intents=intents)

def get_uscf_id_info(uscf_id):
    # Send an HTTP request and get the HTML content
    response = requests.get(uscf_url + "?" + uscf_id)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    print(response.content)
    regular = soup.find_all('input', attrs={'name': 'rating1'})
    quick = soup.find_all('input', attrs={'name': 'rating2'})
    blitz = soup.find_all('input', attrs={'name': 'rating3'})

    if regular:
        regular = re.split('[^0-9]', regular[0]['value'])[0]
    if quick:
        quick = re.split('[^0-9]', quick[0]['value'])[0]
    if blitz:
        blitz = re.split('[^0-9]', blitz[0]['value'])[0]

    string=f"""USCF ID {uscf_id} Has ratings:
\tclassical: {regular}
\tquick: {quick}
\tblitz: {blitz}
"""
    return string


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$help'):
        await message.channel.send("I'm just a baby give me some time to grow")

    if message.content.startswith('$rating'):
        if message.content.rstrip() == "$rating":
            await message.channel.send("Please add a uscf id like \"$rating 123\"")

        uscf_id = re.search(r"\d+", message.content)
        if uscf_id == None:
            print("I didn't understand the command: \"", message.content, "\"")
            await message.channel.send("Couldn't parse uscf id")
            return

        uscf_string = get_uscf_id_info(uscf_id.group())
        await message.channel.send(uscf_string)


uscf_bot_token = os.environ.get("USCF_BOT_TOKEN")
client.run(uscf_bot_token)
