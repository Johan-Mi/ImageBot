#!/usr/bin/env python3
"""This module contains the image bot, which lets you search for images"""

import json
import requests
import discord

PREFIX = "[img]"

client = discord.Client()

with open("key") as key_file:
    key = key_file.read()

url = f"https://pixabay.com/api/?key={key}"


@client.event
async def on_ready():
    """Lets you know when the bot starts."""
    print(f"Discord version: {discord.__version__}")
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    """Responds when someone else sends a message."""
    if message.author == client.user:
        return
    if message.content.startswith(PREFIX):
        search_term = message.content[len(PREFIX):]
        search_response = requests.get(url,
                                       params={
                                           "q": search_term,
                                           "per_page": 3
                                       })
        search_response = json.loads(search_response.content)
        try:
            image_url = search_response["hits"][0]["largeImageURL"]
        except IndexError:
            image_url = "No images found"
        await message.channel.send(image_url)


def main():
    """Runs the bot with the token from the file called 'token'."""
    with open("token") as token_file:
        token = token_file.read()
    client.run(token)


if __name__ == "__main__":
    main()