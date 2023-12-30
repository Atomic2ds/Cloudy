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
from views.core import inviteview, voteview, supportview, documentationview, aboutview
from functions import infoview, handle_help_command
import libraries

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
       await handle_help_command(interaction,type,False)

    @app_commands.command(name="invite",description="Get the link to invite me to your server!")
    async def invite(self, interaction: discord.Interaction):
       await interaction.response.defer()
       await interaction.followup.send(embed=embedutil("invite",None),view=inviteview())

    @app_commands.command(name="support",description="Get the link to the Cloudy support server!")
    async def support(self, interaction: discord.Interaction):
       await interaction.response.defer()
       await interaction.followup.send(embed=embedutil("support",None),view=supportview())

    @app_commands.command(name="vote",description="Get the link to vote for me on top.gg!")
    async def vote(self, interaction: discord.Interaction):
       await interaction.response.defer()
       await interaction.followup.send(embed=embedutil("vote",None),view=voteview())

    @app_commands.command(name="documentation",description="Get the link to our documentation website")
    async def documentation(self, interaction: discord.Interaction):
       await interaction.response.defer()
       await interaction.followup.send(embed=embedutil("documentation",None),view=documentationview())

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
        await interaction.followup.send(embed=embedutil("core","about"),view=aboutview())
     except Exception:
        await interaction.followup.send(embed=embedutil("error",traceback.format_exc())) 

    @app_commands.command(name="update", description="Send an update for Cloudy to the updates channel")
    @app_commands.describe(title="The title of the Update", description="What the update is about", mention="What role to mention on the update message", file="What file to attach to the update")
    async def updateslash(self, interaction: discord.Interaction, title: str, description: str, mention: Optional[discord.Role], file: Optional[discord.Attachment], channel: Optional[discord.TextChannel]):
      try:
         await interaction.response.defer(ephemeral=True)

         if interaction.user.id == 612522818294251522:
           if channel == None:
             channel = self.bot.get_channel(libraries.UPDATE_CHANNEL)
           embed = embedutil("core",("update",f"{title} <:9582_announce:1173479624412508202>",description,interaction))

           if mention:
            content = f"<@&{mention.id}>"
           else:
            content = None

           if content:
            await channel.send(content, embed=embed)
           else:
            await channel.send(embed=embed)

            if file:
                file_data = await file.read()
                file_obj = discord.File(io.BytesIO(file_data), filename=file.filename)
                try:
                   await channel.send(file=file_obj)
                except:
                   pass
            
           await interaction.followup.send(embed=embedutil("success",f"Successfully sent the update for Cloudy"))

         else:
          await interaction.followup.send(embed=embedutil("denied","Only official Cloudy developers have access to this command"))

      except Exception:
         await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))


async def setup(bot):
    await bot.add_cog(core(bot))
