import discord
from discord import ui
import traceback
from embeds import embedutil
import aiohttp
from functions.core import infoview
import libraries
from config import client
import requests

from functions.servers import grab_server_info
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
        description = f"{server_id}"
      options.append(discord.SelectOption(label=name, description=description))
    #  if response.status == 200:
    #    data = response.json()
    #  else:
    #    raise Exception(f"Request to panel failed with status {response.status} for server with id of {server_id} from {panel_url}")
    #  name = data['attributes']['name']
    #  description = data['attributes']['description']
    #  options.append(discord.SelectOption(label=name, description=description))

    #if not options:
    #  options = [discord.SelectOption(label="No Servers Available", description="Use /server add to begin")]

    super().__init__(placeholder="Select a server...", options=options, min_values=1, max_values=1, custom_id="statusserversdropdown")

  async def callback(self, interaction: discord.Interaction):
    pass
