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
from functions.economy import balance_quotes

db = client.fun


class economy(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  Loaded the Economy Cog        ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    @app_commands.command(name="balance",description="View your account balance or someone elses account balance")
    @app_commands.describe(user="Whos you want to see the balance of")
    async def balance(self, interaction: discord.Interaction, user: Optional[discord.User]):

      await interaction.response.defer()
      try:
        if user == None:
            user = interaction.user
        else:
            if user.bot == True:
              await interaction.followup.send(embed=embedutil("denied","Bots don't have bank accounts!"),ephemeral=True)
              return

        if not db.wallets.find_one({"user": user.id}):
            db.wallets.insert_one({"user": user.id, "value": 0})

        document = db.wallets.find_one({"user":  user.id})
        balance = document["value"]

        if user == interaction.user:
            title = "Personal account balance"
            description = f"You currently have ${balance} in your bank account"
            footer = balance_quotes(balance)
        else:
            title = f"{user.name.capitalize()}'s Account Balance"
            description = f"They currently have ${balance} in their bank account"
            footer = "This is not your bank account"
            if balance < 20:
                footer = footer + " (Surprisingly)"

        embed = discord.Embed(colour=0x4c7fff, title=title, description=description)
        embed.set_footer(text=footer)

        await interaction.followup.send(embed=embed)

      except Exception:
          await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))



async def setup(bot):
    await bot.add_cog(economy(bot))

