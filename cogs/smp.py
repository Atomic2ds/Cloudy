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

from views.smp import link_smp_server, smp_status_view, smp_panel_view
from functions.smp import fetch_server_info, fetch_server_resources, send_detailed_Stats, send_smp_info
from views.core import infoview
db = client.smp


class smp(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  Loaded the SMP Cog            ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    smp_cmd = app_commands.Group(name="smp", description="Link an smp server with your discord community easily")



    @smp_cmd.command(name="link",description="Link an smp server using the pterodactyl api")
    #@app_commands.describe(name="What you would like to name your SMP, is not connected to its name on your panel",description="Describe your smp server, will only be shown to people on discord")
    async def link(self, interaction: discord.Interaction):#, name: str, description: str):
       try:
        if not interaction.permissions.manage_guild:
          await interaction.response.send_message(embed=embedutil("denied","You don't have permissions to run this command!"),ephemeral=True)
          return
        
        if db.config.find_one({"guild_id": interaction.guild.id}):
          await interaction.response.send_message(embed=embedutil("denied","You already have an SMP linked, use `/smp unlink` to link a new one"),ephemeral=True)
          return
        
        await interaction.response.send_modal(link_smp_server())

       except Exception:
          await interaction.response.send_message(embed=embedutil("error",traceback.format_exc()),ephemeral=True)

    @smp_cmd.command(name="status",description="View stats about the SMP, like CPU used, RAM used and Disk Space used up")
    async def stats(self, interaction: discord.Interaction):
        await send_detailed_Stats(interaction, False)

    @smp_cmd.command(name="info",description="See some more detailed information about the smp server, like location, node, limits and more")
    async def stats(self, interaction: discord.Interaction):
        await send_smp_info(interaction, False)

    @smp_cmd.command(name="unlink",description="Disconnect the currently connected smp server from your community")
    async def unlink(self, interaction: discord.Interaction):
       try:

        if not interaction.permissions.manage_guild:
            await interaction.response.send_message(embed=embedutil("denied","You don't have permissions to run this command!"),ephemeral=True)
            return

        if not db.config.find_one({"guild_id": interaction.guild.id}):
            await interaction.response.send_message(embed=embedutil("denied","There is currently no server linked to your discord community"),ephemeral=True)
            return

        db.config.delete_many({"guild_id":interaction.guild.id})
        await interaction.response.send_message(embed=embedutil("success","Successfully unlinked your currently linked SMP server"),ephemeral=True)

       except Exception:
           await interaction.response.send_message(embed=embedutil("error",traceback.format_exc()),ephemeral=True)

    @smp_cmd.command(name="add",description="Add an extra server to the smp module")
    async def add(self, interaction: discord.Interaction):
       await interaction.response.send_message(embed=embedutil("simple","This is still a work in progress, if your a big community or more than just 1 smp than we reccomend our server linker, which has much more features. The smp module is just designed for small or friend group communities"),ephemeral=True)


    @smp_cmd.command(name="panel",description="Send a panel where members can view status and info of your smp server")
    @app_commands.describe(channel="Where you want your smp panel to be located/sent")
    async def panel(self, interaction: discord.Interaction, channel: Optional[discord.TextChannel]):
     try:
      if not interaction.permissions.manage_guild:
            await interaction.response.send_message(embed=embedutil("denied","You don't have permissions to run this command!"),ephemeral=True)
            return
      
      await interaction.response.defer(ephemeral=True)

      if channel == None:
         channel = interaction.channel
      await channel.send(embed=embedutil("smp",interaction),view=smp_panel_view())

      await interaction.followup.send(embed=embedutil("success",f"Successfully sent your servers SMP panel to {channel.mention}"))
     except Exception:
        await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))

async def setup(bot):
    await bot.add_cog(smp(bot))

