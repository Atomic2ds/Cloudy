
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


# -- Processing Autoroles --
async def handle_autoroles(member):
 if member.bot == False:
  try:
    cursor = client.utils.autoroles.find({"guild_id": member.guild.id,})
    for document in cursor:
      roles = document["human_roles"]
      for item in roles:
        role = discord.utils.get(member.guild.roles,id=item)
        await member.add_roles(role)
  except Exception:
    print(traceback.format_exc())
 if member.bot == True:
   try:
    cursor = client.utils.autoroles.find({"guild_id": member.guild.id,})
    for document in cursor:
      roles = document["bot_roles"]
      for item in roles:
        role = discord.utils.get(member.guild.roles,id=item)
        await member.add_roles(role)
   except Exception as e:
    print(traceback.format_exc())