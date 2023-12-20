import pymongo
import requests
import json
from embeds import embedutil
import traceback
from config import bot
from config import client
import aioschedule
from functions import infoview

async def daily_task():
    embed = embedutil("fact","Fact of the day")
    for guild in bot.guilds:
      try:
       cursor = client.fact.config.find({"guild_id": guild.id,})
       for document in cursor:
          channel = document["channel_id"]
          channel = bot.get_channel(channel)
          await channel.send(embed=embed,view=infoview("Automated message"))
      except:
        pass
        continue
      
