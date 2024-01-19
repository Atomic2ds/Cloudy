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
from discord import ui

from functions.basements import sell_basement_item_function

class storeview(discord.ui.View):
   def __init__(self):
      super().__init__(timeout=None)

   @discord.ui.button(label="Buy Item", style=discord.ButtonStyle.gray, custom_id="buy_item_basements")
   async def buy_basement_item(self, interaction: discord.Interaction, button: discord.ui.Button):
      await interaction.response.send_message(embed=embedutil("denied","This feature is still a work in progress"),ephemeral=True)

   @discord.ui.button(label="Sell Item", style=discord.ButtonStyle.gray, custom_id="sell_item_basements")
   async def sell_basement_item(self, interaction: discord.Interaction, button: discord.ui.Button):
      await interaction.response.send_modal(sell_item())

   
class sell_item(ui.Modal, title="Sell Basement Item"):

    name = ui.TextInput(label="Item Name", placeholder="The name of something already in your basement", style=discord.TextStyle.short, required=True)
    value = ui.TextInput(label="Item Value", placeholder="How much you want to sell the item for", style=discord.TextStyle.short, required=True)

    async def on_submit(self, interaction: discord.Interaction):
     await sell_basement_item_function(interaction, str(self.name), str(self.value))
