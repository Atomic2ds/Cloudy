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


class hyperlink_button(discord.ui.View):
   def __init__(self, link: str,label: str):
      super().__init__()
      self.inv = link
      self.label = label
      self.add_item(discord.ui.Button(label=self.label, url=self.inv))

async def handle_help_command(interaction, type, ephemeral):
   await interaction.response.defer()
   try:
       from views.core import helpoverview
       if not type == None:
        await interaction.followup.send(embed=embedutil("help",type),view=helpoverview(),ephemeral=ephemeral)
       else:
        await interaction.followup.send(embed=embedutil("help","overview"),view=helpoverview(),ephemeral=ephemeral)
   except Exception:
         await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),ephemeral=ephemeral)

class requestedby(discord.ui.View):
   def __init__(self, user: discord.User):
      super().__init__()
      self.user = user
      self.add_item(discord.ui.Button(label=f"Requested by {self.user.name.capitalize()}",style=discord.ButtonStyle.gray, disabled=True))
