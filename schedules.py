import pymongo
import requests
import json
from embeds import embedutil
import traceback
from config import bot
from config import client
import aioschedule

async def daily_task():
    embed = embedutil("fact","Fact of the day")
    for guild in bot.guilds:
      try:
       cursor = client.fact.config.find({"guild_id": guild.id,})
       for document in cursor:
          channel = document["channel_id"]
          channel = bot.get_channel(channel)
          await channel.send(embed=embed)
      except:
        pass
        continue
      
aioschedule.every().day.at("1:32").do(daily_task)