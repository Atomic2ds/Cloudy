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

db = client.fun

async def sell_basement_item_function(interaction, name, value):
        await interaction.response.defer()
        try:

            if db.basement_store.find_one({"user_id": interaction.user.id, "name":name}):
                await interaction.followup.send(embed=embedutil("denied",f"That person is already up for sale!"))
                return
            
            document = db.basements.find_one({"id":interaction.user.id,"name":name})
            description = document["description"]
            db.basements.delete_many({"name": name,"id":interaction.user.id})
            db.basement_store.insert_one({"user_id": interaction.user.id,"name":name,"description": description,"value":value})

            await interaction.followup.send(embed=embedutil("success",f"Successfully set {name} to be up for sale!"))
        except Exception:
            await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))