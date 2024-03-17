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
import libraries
from datetime import timedelta
import datetime
from embeds import embedutil
from config import client
import pymongo
from functions.core import requestedby

db = client.fun


class quotes(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  Loaded the Quotes Cog        ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    quote_cmd = app_commands.Group(name="quote", description="Configure the quotes module")

    @quote_cmd.command(name="channel",description="Set the channel where quotes are sent to")
    @app_commands.describe(option="What channel you want quotes to be sent to")
    async def quote_channel(self, interaction: discord.Interaction, option: discord.TextChannel):
        await interaction.response.defer(ephemeral=True)
        try:
         if interaction.user.guild_permissions.manage_guild:
          channel = option
          if db.quotes.find_one({"guild_id": interaction.guild.id}):
            db.quotes.update_one({"guild_id": interaction.guild.id},{"$set": {"channel_id": channel.id}})
          else:
            db.quotes.insert_one({"guild_id": interaction.guild.id,"channel_id": channel.id})
          await channel.send(embed=embedutil("quotes","configured"),view=requestedby(interaction.user))
          await interaction.followup.send(embed=embedutil("success",f"Successfully set {channel.mention} as the quotes channel!"))
         else:
            await interaction.followup.send(embed=embedutil("denied","Your don't have permission to run this command"))
        except Exception:
            await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))


async def setup(bot):
    await bot.add_cog(quotes(bot))

