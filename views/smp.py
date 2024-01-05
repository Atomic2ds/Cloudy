import discord
from discord import ui
import traceback
from embeds import embedutil
import aiohttp
from functions.core import infoview
import libraries
from config import client

from functions.smp import fetch_server_info, fetch_server_resources, send_detailed_Stats
db = client.smp

class link_smp_server(ui.Modal, title="Link SMP Server"):

    panel_url = ui.TextInput(label="Panel URL", placeholder="The url of your providers panel (Without the https://)", style=discord.TextStyle.short, required=True)
    server_id = ui.TextInput(label="Server ID", placeholder="Get this under debug information on the settings page", style=discord.TextStyle.short, required=True)
    api_key = ui.TextInput(label="API Key", placeholder="Go to your providers api credentials page under account", style=discord.TextStyle.short, required=True)

    async def on_submit(self, interaction: discord.Interaction):
     await interaction.response.defer()
     try:

        api_key = str(self.api_key)
        server_id = str(self.server_id)
        panel_url = str(self.panel_url)

        headers = {
          'Authorization': f'Bearer {api_key}',
          'Accept': 'application/vnd.pterodactyl.v1+json'
        }
        data = await fetch_server_info(panel_url, server_id, headers)
        name = data['attributes']['name']
        description = data['attributes']['description']
        
        
        db.config.insert_one({"guild_id": interaction.guild.id, "api_key": api_key, "panel_url": panel_url, "server_id": server_id})
        embed = embedutil("simple",f"Successfully linked your smp server to your discord!")
        await interaction.followup.send(embed=embed,ephemeral=True)

     except Exception:
        await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),ephemeral=True)



class smp_status_view(discord.ui.View):
   def __init__(self):
      super().__init__(timeout=None)

   @discord.ui.button(label="Detailed Stats", style=discord.ButtonStyle.gray, custom_id="detilaed_stats_status_embed", emoji="📊")
   async def detailedstats(self, interaction: discord.Interaction, button: discord.ui.Button):
      await send_detailed_Stats(interaction, True)

   #@discord.ui.button(label="Server Info", style=discord.ButtonStyle.gray, custom_id="server_info_status_embed", emoji="🌍")
   #async def serverinfo(self, interaction: discord.Interaction, button: discord.ui.Button):
   #   pass