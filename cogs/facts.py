import discord
from discord.ext import commands
#from utils import embedutil
from discord import app_commands, ui, Webhook
import aiohttp
import datetime
global bot
from config import bot
from discord.app_commands import Choice
import pymongo
import random
from embeds import embedutil
import requests
import traceback
import json
from config import client
from views.facts import factview
from functions.core import requestedby

db = client.fact

class fact(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  Loaded the Facts Cog          ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")


    fact_cmd = app_commands.Group(name="fact", description="Set a fact of the day channel")

    @fact_cmd.command(name="channel", description="Choose where daily facts will be sent to")
    async def fact_channel(self, interaction: discord.Interaction, option: discord.TextChannel):
       try:
         if interaction.user.guild_permissions.manage_guild:
          await interaction.response.defer()
          if db.config.find_one({"guild_id": interaction.guild.id}):
            db.config.update_one({"guild_id": interaction.guild.id},{"$set": {"channel_id": option.id}})
          else:
            db.config.insert_one({"guild_id": interaction.guild.id,"channel_id": option.id})
          await option.send(embed=embedutil("simple","This channel has succesfully been setup as a daily facts channel!"),view=requestedby(interaction.user))
          await interaction.followup.send(embed=embedutil("success",f"Successfully set {option.mention} as the fact of the day channel!"))
         else:
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send(embed=embedutil("bot",["error","You don't have permission to use this command!"], interaction.user, interaction.guild))
       except Exception:
          await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),ephemeral=True)
    
    @fact_cmd.command(name="disable",description="Disable the fact of the day channel")
    async def disable(self, interaction: discord.Interaction):
     await interaction.response.defer()
     try:
      if not db.ows.find_one({"guild_id": interaction.guild.id}):
        await interaction.followup.send(embed=embedutil("denied","The fact channel is not configured yet!"))
        return
      if interaction.permissions.manage_guild:
          if db.config.find_one({"guild_id": interaction.guild.id}):
            db.config.update_one({"guild_id": interaction.guild.id},{"$set": {"enabled": False}})
          else:
            db.config.insert_one({"guild_id": interaction.guild.id,"channel_id": interaction.user})
          cursor = client.fun.ows.find({"guild_id": interaction.guild.id})
          for document in cursor:
            channel = self.bot.get_channel()
          await interaction.followup.send(embed=embedutil("success","Successfully disabled the fact of the day channel!"))
      else:
          await interaction.followup.send(embed=embedutil("error","You don't have permission to run this command!"),ephemeral=True)
     except Exception:
       await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),ephemeral=True)

    @fact_cmd.command(name="random",description="Generate a random fact")
    async def random(self, interaction: discord.Interaction):
      await interaction.response.defer()
      try:
        await interaction.followup.send(embed=embedutil("fact","Random Fact"),view=factview(interaction.user.name.capitalize()))
      except Exception:
         await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),ephemeral=True)

    @fact_cmd.command(name="trigger",description="Forcefully trigger a daily fact")
    async def trigger(self, interaction: discord.Interaction):
     await interaction.response.defer()
     try:
      if interaction.user.id == 612522818294251522:
       from schedules import daily_task
       await daily_task()
       await interaction.followup.send(embed=embedutil("simple","Successfully triggered a daily fact everywhere!"))
     except Exception:
       await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),ephemeral=True)


async def setup(bot):
    await bot.add_cog(fact(bot))
