from config import client, bot
import discord
import random
from embeds import embedutil
import traceback
import requests
import config
import aiohttp
import asyncio
import json
from views.core import infoview
import libraries


async def process_img2text(msg):
  if msg.author.bot == False:
    cursor = client.images.config.find({"channel_id": msg.channel.id})
    for document in cursor:
       status = document["status"]
    if status:
       if status == "enabled":
        try:
          embed = await img2text(msg.content)
          await msg.reply(embed=embed, mention_author=False)
        except Exception:
          embed = embedutil("error",traceback.format_exc())
          await msg.reply(embed=embed,mention_author=False)

async def img2text(query):
    try:
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=15&page=1"
        headers = {"Authorization": config.PEXELS_API}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response_data = await response.json()

        embed = discord.Embed(colour=0x4c7fff, description=f"Prompt: {query}")
        embed.set_footer(text="Sourced from pexels.com")

        if "photos" in response_data:
            photos = response_data["photos"]
            if len(photos) > 0:
                embed.set_image(url=random.choice(photos)["src"]["original"])
                return embed
            
        embed = embedutil("denied", "Unable to find an image based on your query")
        return embed

    except Exception:
        return embedutil("error", traceback.format_exc())