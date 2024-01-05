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
        await interaction.response.defer()
        try:
            if db.basements.find_one({"id": interaction.user.id, "name": name}):
                await interaction.followup.send(embed=embedutil("denied","That person already exists in your basement"))
                return
            db.basements.insert_one({"id": interaction.user.id,"name": name,"description": description,})
            await interaction.followup.send(embed=embedutil("success",f"Successfully added `{name}` to your basement"))
        except Exception:
            await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))

    #Remove someone from your basement
    @basement_cmd.command(name="remove", description="Remove someone from your basement")
    @app_commands.describe(name="The name of the person to remove from your basement")
    async def add(self, interaction: discord.Interaction, name: str):
        await interaction.response.defer()
        try:
            result = db.basements.delete_many({"name": name})
            await interaction.followup.send(embed=embedutil("success",f"Successfully removed `{name}` from your basement"))
        except Exception:
            await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))

async def setup(bot):
    await bot.add_cog(basements(bot))