import discord
from discord.ext import commands
from discord import app_commands
import random
from typing import Optional
import os
from discord.app_commands import Choice
import datetime
import json
import traceback
import io
import requests
import config
from embeds import embedutil
import aiohttp
from views.core import inviteview, voteview
from functions import infoview

class core(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  Loaded the Core Cog           ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    @app_commands.command(name="help",description="View all commands on the Cloudy Bot")
    @app_commands.choices(type=[
      Choice(name="Core commands", value="core"),
      Choice(name="Fun commands", value="fun"),
      Choice(name="Duck commands", value="duck"),
      Choice(name="Utility commands", value="utility"),
      Choice(name="Fact commands", value="fact"),
      Choice(name="Story Commands", value="story"),
    ])
    @app_commands.describe(type="What type of commands to look at")
    async def help(self, interaction: discord.Interaction, type: Optional[str]):
      await interaction.response.defer()
      try:
       from views.core import helpoverview
       if not type == None:
        await interaction.followup.send(embed=embedutil("help",type),view=helpoverview())
       else:
        await interaction.followup.send(embed=embedutil("help","overview"),view=helpoverview())
      except Exception:
         await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))

    @app_commands.command(name="invite",description="Get the link to invite me to your server!")
    async def invite(self, interaction: discord.Interaction):
       await interaction.response.defer()
       await interaction.followup.send(embed=embedutil("invite",None),view=inviteview())

    @app_commands.command(name="vote",description="Get the link to vote for me on top.gg!")
    async def vote(self, interaction: discord.Interaction):
       await interaction.response.defer()
       await interaction.followup.send(embed=embedutil("vote",None),view=voteview())

    @app_commands.command(name="ping", description="Health check, view system ping")
    async def duck(self, interaction: discord.Interaction):
     try:
        await interaction.response.defer()
        await interaction.followup.send(embed=embedutil("core","ping"))
     except Exception:
        await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))

    @app_commands.command(name="about",description="View basic information about the Cloudy Bot")
    async def about(self, interaction: discord.Interaction):
     try:
        await interaction.response.defer()
        await interaction.followup.send(embed=embedutil("core","about"))
     except Exception:
        await interaction.followup.send(embed=embedutil("error",traceback.format_exc())) 


async def setup(bot):
    await bot.add_cog(core(bot))
