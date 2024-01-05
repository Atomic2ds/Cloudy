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



async def fetch_gif(query):
  try:
   session = aiohttp.ClientSession()

   if query == None:
      response = await session.get(f'https://api.giphy.com/v1/gifs/random?api_key={config.GIPHY_KEY}')
      data = json.loads(await response.text())
      embed = embedutil("gif",(None,"Random Gif",data['data']['images']['original']['url']))

   else:
      search = query.replace(' ', '+')
      response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + f'&api_key={config.GIPHY_KEY}')
      data = json.loads(await response.text())
      gif_choice = random.randint(0, 9)
      embed = embedutil("gif",(query,"Custom Gif",data['data'][gif_choice]['images']['original']['url']))

  except Exception:
     embed = embedutil("error",traceback.format_exc())

  await session.close()
  return embed


async def define(term):
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    headers = {
      "X-RapidAPI-Key": "09efa8afd5msh469606e5298e21cp14d14ajsnfd148325b4b2"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params={"term": term}) as response:
            data = await response.json()

    if len(data["list"]) > 0:
        definition = data["list"][0]["definition"]
        return definition
    else:
        return "Sorry, I couldn't find a definition for that term."
    
async def get_definition(word):
  try:
    response = await define(word)
    embed=embedutil("definition",(word,response))
  except Exception:
    embed=embedutil("error",traceback.format_exc())
  
  return embed