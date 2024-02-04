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

from functions.servers import grab_server_info, send_server_status, server_info_embed
from functions.core import infoview
db = client.servers

class statusserversview(discord.ui.View):
   def __init__(self, guild_id: str, category: str):
      super().__init__(timeout=None)
      self.add_item(statusserversdropdown(guild_id,category))

class statusserversdropdown(discord.ui.Select):
  def __init__(self, guild_id: str, category: str):
    self.guild_id = guild_id
    self.category = category
    options = []

    if category == None:
      query = ({"guild_id": self.guild_id,})
    else:
      query = ({"guild_id": self.guild_id,"category": category})
    

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
      db.list.update_one({"server_id": server_id}, {"$set": {"description": description}})
      options.append(discord.SelectOption(label=name, description=description))

    if not options:
      options = [discord.SelectOption(label="No Servers Available", description="Add one using /server add")]

    super().__init__(placeholder="Select a server...", options=options, min_values=1, max_values=1, custom_id="statusserversdropdown")




  async def callback(self, interaction: discord.Interaction):
   await interaction.response.defer()

   try:
    if self.values[0] == "No Servers Available":
     await interaction.followup.send(embed=embedutil("denied","You need to add a server before you can view the status of one!"),ephemeral=True)
     return


    data = await server_info_embed(self.values[0],interaction.guild.id)
    embed = data[0]

    #await interaction.followup.send(embed=embed,ephemeral=True)
    await interaction.followup.edit_message(embed=embed,message_id=interaction.message.id,view=serverstatusview(data[1]))

   except Exception:
     await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),ephemeral=True)




class serverstatusview(discord.ui.View):
  def __init__(self, label: str):
     self.label = label
     super().__init__(timeout=None)
     #self.add_item(discord.ui.Button(label=self.label,style=discord.ButtonStyle.gray, disabled=True))

  @discord.ui.button(label="Go Back", style=discord.ButtonStyle.gray, custom_id="gobacktoserverlist")
  async def gobacktostatuslist(self, interaction: discord.Interaction, button: discord.ui.Button):
       if not interaction.permissions.manage_guild:
        await interaction.response.send_message(embed=embedutil("denied","You don't have permissions to run this command!"),ephemeral=True)
        return
       await interaction.response.defer()
       try:
         await interaction.followup.edit_message(embed=embedutil("servers","status"),view=statusserversview(interaction.guild.id,None),message_id=interaction.message.id)
       except Exception:
          await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))




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
      max_values = 1
    else:
      max_values = db.list.count_documents({"guild_id": guild_id})

    super().__init__(placeholder="Select a server...", options=options, min_values=1, max_values=max_values, custom_id="deleteserversdropdown")

  async def callback(self, interaction: discord.Interaction):
   if not interaction.permissions.manage_guild:
      await interaction.response.send_message(embed=embedutil("denied","You don't have permissions to run this command!"),ephemeral=True)
      return
   await interaction.response.defer()
   try:
    print(self.values)
    for server in self.values:
      name = server
      query = {"name": name,"guild_id":interaction.guild.id}
      db.list.delete_many(query)
      
    await interaction.followup.send(embed=embedutil("success","Successfully deleted your selected server(s) off the system"),ephemeral=True)
    await interaction.followup.edit_message(message_id=interaction.message.id,view=deleteserversview(interaction.guild.id))


   except Exception:
     await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),ephemeral=True)

class select_servers_view(discord.ui.View):
   def __init__(self, guild_id: str, name: str, description: str, channel):
      super().__init__(timeout=None)
      self.add_item(selectserversdropdown(guild_id,name,description,channel))

class selectserversdropdown(discord.ui.Select):
  def __init__(self, guild_id: str, name: str, description: str, channel):
    self.name = name
    self.guild_id = guild_id
    self.description = description
    self.channel = channel
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
      db.list.update_one({"server_id": server_id}, {"$set": {"description": description}})
      options.append(discord.SelectOption(label=name, description=description))

    if not options:
      options = [discord.SelectOption(label="No Servers Available", description="Add one using /server add")]
      max_values = 1
    else:
      max_values = db.list.count_documents({"guild_id": guild_id})

    super().__init__(placeholder="Select a server...", options=options, min_values=1, max_values=max_values, custom_id="deleteserversdropdown")

  async def callback(self, interaction: discord.Interaction):
   if not interaction.permissions.manage_guild:
      await interaction.response.send_message(embed=embedutil("denied","You don't have permissions to run this command!"),ephemeral=True)
      return
   await interaction.response.defer()
   try:
    #await interaction.followup.send(embed=embedutil("success","Successfully deleted your selected server(s) off the system"),ephemeral=True)
    #await interaction.followup.edit_message(message_id=interaction.message.id,view=deleteserversview(interaction.guild.id))
     max_values = db.list.count_documents({"guild_id": interaction.guild.id})
     #print(self.values)
     values = []
     for server in self.values:
      for document in db.list.find({"guild_id": self.guild_id,"name":server}):
        name = document["name"]
        description = document["description"]
      values.append(discord.SelectOption(label=name, description=description))

     #print(values)
        
     await self.channel.send(embed=embedutil("serverpanel",(self.name,self.description)),view=server_panel_view(values,max_values))


   except Exception:
     await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),ephemeral=True)



class server_panel_view(discord.ui.View):
   def __init__(self, options, max_values):
      super().__init__(timeout=None)
      self.add_item(serverpanel(options,max_values))


class serverpanel(discord.ui.Select):
  def __init__(self, options, max_values):

    super().__init__(placeholder="Select a server...", options=options, custom_id="serverpaneldropdwon")

  async def callback(self, interaction: discord.Interaction):
   await interaction.response.defer()
   try:
    data = await server_info_embed(self.values[0],interaction.guild.id)
    embed = data[0]

    await interaction.followup.send(embed=embed,ephemeral=True)


   except Exception:
     await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),ephemeral=True)
