import discord
from discord.ext import commands
from discord import app_commands, ui
import random
from discord.app_commands import Choice
import aiohttp
import requests
from typing import Optional
import json
import traceback
import os
from discord import Webhook
from datetime import timedelta
import datetime
from embeds import embedutil
from config import client

from functions.basements import sell_basement_item_function
from views.basements import storeview

db = client.fun


class basements(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  Loaded the Basements Cog      ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    basement_cmd = app_commands.Group(name="basement", description="Configure your basement")

    #View someone elses basement
    @basement_cmd.command(name="view", description="View someones basement")
    @app_commands.describe(user="Whos basement you want to view")
    async def notes(self, interaction: discord.Interaction, user: Optional[discord.User]):
        try:
          await interaction.response.defer()
          await interaction.followup.send(embed=embedutil("basement",(interaction,user)))
        except Exception:
            await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))

    #Add shit to your basement
    @basement_cmd.command(name="add", description="Add someone to your basement")
    @app_commands.describe(name="The name of the person", description="Why they are in your basement or something like that")
    async def add(self, interaction: discord.Interaction, name: str, description: str):
        try:
            if db.basements.find_one({"id": interaction.user.id, "name": name}):
                await interaction.response.send_message(embed=embedutil("denied","That person already exists in your basement"),ephemeral=True)
                return
            if db.basements.count_documents({"id": interaction.user.id}) == 25:
              await interaction.followup.send(embed=embedutil("denied","You have reached the limit on how many people you can have in your basement!"),ephemeral=True)
              return
            await interaction.response.defer()
            db.basements.insert_one({"id": interaction.user.id,"name": name,"description": description,})
            await interaction.followup.send(embed=embedutil("success",f"Successfully added {name} to your basement"))
        except Exception:
            await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))

    #Remove someone from your basement
    @basement_cmd.command(name="remove", description="Remove someone from your basement")
    @app_commands.describe(name="The name of the person to remove from your basement")
    async def add(self, interaction: discord.Interaction, name: str):
        await interaction.response.defer()
        try:
            result = db.basements.delete_many({"name": name,"id":interaction.user.id})
            await interaction.followup.send(embed=embedutil("success",f"Successfully removed {name} from your basement"))
        except Exception:
            await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))

    #Sell something from your basement
    @basement_cmd.command(name="sell", description="Sell someone from your basement")
    @app_commands.describe(name="The name of the person to sell from your basement",value="How much you want to sell your item for")
    async def sell(self, interaction: discord.Interaction, name: str, value: int):
        await sell_basement_item_function(interaction, str(self.name), str(self.value))

    #Remove something from the basement store
    @basement_cmd.command(name="unsell", description="Remove something from the Cloudy basement store")
    @app_commands.describe(name="The name of the person to remove from the Cloudy basement store")
    async def sell(self, interaction: discord.Interaction, name: str):
        await interaction.response.defer()
        try:
            if not db.basement_store.find_one({"user_id": interaction.user.id, "name":name}):
                await interaction.followup.send(embed=embedutil("denied",f"That person is not up for sale!"))
                return
            
            document = db.basement_store.find_one({"user_id":interaction.user.id,"name":name})
            description = document["description"]
            db.basements.insert_one({"id": interaction.user.id,"name":name,"description": description})
            db.basement_store.delete_many({"name": name,"user_id":interaction.user.id})
            await interaction.followup.send(embed=embedutil("success",f"Successfully removed {name} from the basement store!"))
        except Exception:
            await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))

    #View the basement store
    @basement_cmd.command(name="store", description="View the basement store, the place you can buy stuff for your basement")
    async def sell(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            embed = discord.Embed(colour=0x4c7fff, title="Basement Store", description="Everything on here is sold by users, nothing here is controlled by Cloudy itself")
            cursor = db.basement_store.find({})
            for document in cursor:
              name = document["name"]
              description = document["description"]
              embed.add_field(name=name, value=description)
            if db.basement_store.count_documents({}) < 1:
                embed.set_footer(text="There is currently nothing in the store")
            else:
                embed.set_footer(text="Use the buttons below to buy stuff")
            await interaction.followup.send(embed=embed,view=storeview())
        except Exception:
            await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))

    @basement_cmd.command(name="buy",description="Buy something from the basement store")
    async def buy(self, interaction: discord.Interaction, name: str):
        await interaction.response.send_message(embed=embedutil("denied","This feature is still a work in progress"),ephemeral=True)


async def setup(bot):
    await bot.add_cog(basements(bot))