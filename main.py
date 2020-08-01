#!/usr/bin/env python3
"""This module contains the image bot, which lets you search for images"""

import json
import requests
import urllib.parse
import discord

PREFIX = "[img]"

client = discord.Client()

with open("key") as key_file:
    key = key_file.read()

url = f"https://pixabay.com/api/?key={key}&per_page=3"


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
        search_url = f"{url}&q={urllib.parse.quote(search_term)}"
        print(search_url)
        search_response = requests.get(search_url)
        try:
            search_response = json.loads(search_response.content)
            try:
                image_url = search_response["hits"][0]["largeImageURL"]
            except IndexError:
                image_url = "No images found"
            await message.channel.send(image_url)
        except Exception as err:
            print(search_response.content)
            await message.channel.send(str(err))


def main():
    """Runs the bot with the token from the file called 'token'."""
    with open("token") as token_file:
        token = token_file.read()
    client.run(token)


if __name__ == "__main__":
    main()
