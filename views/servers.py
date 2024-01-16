import discord
from discord import ui
import traceback
from embeds import embedutil
import aiohttp
from functions.core import infoview
import libraries
from config import client
import requests
import random

from functions.servers import grab_server_info, send_server_status
from functions.core import infoview
db = client.servers

class statusserversview(discord.ui.View):
   def __init__(self, guild_id: str):
      super().__init__(timeout=None)
      self.add_item(statusserversdropdown(guild_id))

class statusserversdropdown(discord.ui.Select):
  def __init__(self, guild_id: str):
    self.guild_id = guild_id
    options = []


    for document in db.list.find({"guild_id": self.guild_id,}):
      api_key = document["api_key"]
      panel_url = document["panel_url"]
      server_id = document["server_id"]
#
      headers = {'Authorization': f'Bearer {api_key}','Accept': 'application/vnd.pterodactyl.v1+json'}
      response = requests.get(f"https://{panel_url}/api/client/servers/{server_id}", headers=headers)
      data = response.json()
      try:
        name = data['attributes']['name']
        description = data['attributes']['description']
      except:
        name = f"Unavailable ({panel_url})"
        description = server_id
      db.list.update_one({"server_id": server_id}, {"$set": {"name": name}})
      options.append(discord.SelectOption(label=name, description=description))

    if not options:
      options = [discord.SelectOption(label="No Servers Available", description="Add one using /server add")]

    super().__init__(placeholder="Select a server...", options=options, min_values=1, max_values=1, custom_id="statusserversdropdown")




  async def callback(self, interaction: discord.Interaction):
   await interaction.response.defer()
   try:
    name = self.values[0]
    query = {"name": name}
    results = db.list.find(query)
    
    for document in results:
      api_key = document["api_key"]
      panel_url = document["panel_url"]
      server_id = document["server_id"]

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }
    response = requests.get(f"https://{panel_url}/api/client/servers/{server_id}", headers=headers)
    data = response.json()
    name = data['attributes']['name']
    description = data['attributes']['description']

    response2 = requests.get(f"https://{panel_url}/api/client/servers/{server_id}/resources", headers=headers)
    stats = response2.json()

    state = stats['attributes']['current_state']
    memory_bytes = stats['attributes']['resources']['memory_bytes']
    cpu_absolute = stats['attributes']['resources']['cpu_absolute']
    disk_bytes = stats['attributes']['resources']['disk_bytes']
    network_tx_bytes = stats['attributes']['resources']['network_tx_bytes']
    network_rx_bytes = stats['attributes']['resources']['network_rx_bytes']
    uptime = stats['attributes']['resources']['uptime']
    

    embed = discord.Embed(colour=0x4c7fff, title=name, description=description)

    embed.add_field(name="State", value=state.capitalize())
    embed.add_field(name="Memory Usage", value=f"{bytes_to_gb(memory_bytes)}GiB")
    embed.add_field(name="CPU Usage", value=f"{str(cpu_absolute)}%")
    embed.add_field(name="Disk Usage", value=f"{bytes_to_gb(disk_bytes)}GiB")
    embed.add_field(name="Network RX", value=f"{bytes_to_mb(network_rx_bytes)}MiB")
    embed.add_field(name="Network TX", value=f"{bytes_to_mb(network_tx_bytes)}MiB")

    embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)

    await interaction.followup.send(embed=embed,view=infoview(f"Server ID: {server_id}"),ephemeral=True)
    await interaction.followup.edit_message(message_id=interaction.message.id,view=statusserversview(interaction.guild.id))

   except Exception:
     await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),ephemeral=True)




def bytes_to_mb(bytes):
    """Convert bytes to megabytes and round to 4 decimal places."""
    return round(bytes / (2**20), 2)

def bytes_to_gb(bytes):
    """Convert bytes to gigabytes and round to 4 decimal places."""
    return round(bytes / (2**30), 2)



class deleteserversview(discord.ui.View):
   def __init__(self, guild_id: str):
      super().__init__(timeout=None)
      self.add_item(deleteserversdropdown(guild_id))

class deleteserversdropdown(discord.ui.Select):
  def __init__(self, guild_id: str):
    self.guild_id = guild_id
    options = []


    for document in db.list.find({"guild_id": self.guild_id,}):
      api_key = document["api_key"]
      panel_url = document["panel_url"]
      server_id = document["server_id"]
#
      headers = {'Authorization': f'Bearer {api_key}','Accept': 'application/vnd.pterodactyl.v1+json'}
      response = requests.get(f"https://{panel_url}/api/client/servers/{server_id}", headers=headers)
      data = response.json()
      try:
        name = data['attributes']['name']
        description = data['attributes']['description']
      except:
        name = f"Unavailable ({panel_url})"
        description = server_id
      db.list.update_one({"server_id": server_id}, {"$set": {"name": name}})
      options.append(discord.SelectOption(label=name, description=description))

    if not options:
      options = [discord.SelectOption(label="No Servers Available", description="Add one using /server add")]

    super().__init__(placeholder="Select a server...", options=options, min_values=1, max_values=db.list.count_documents({"guild_id": guild_id}), custom_id="deleteserversdropdown")

  async def callback(self, interaction: discord.Interaction):
   await interaction.response.defer()
   try:
    print(self.values)
    for server in self.values:
      name = server
      query = {"name": name}
      db.list.delete_many(query)
      
    await interaction.followup.send(embed=embedutil("success","Successfully deleted your selected server(s) off the system"),ephemeral=True)
    await interaction.followup.edit_message(message_id=interaction.message.id,view=deleteserversview(interaction.guild.id))


   except Exception:
     await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),ephemeral=True)