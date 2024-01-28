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
from views.art import submission_buttons
from functions.core import requestedby

db = client.fun


class art(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  Loaded the Art Cog            ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    art_cmd = app_commands.Group(name="art", description="Commands related to the Art Module")

    


    @art_cmd.command(name="configure",description="Setup the art module quickly and easily")
    @app_commands.describe(submissions_channel="The place where moderators and admins accept or deny art submissions",showcase_channel="The place where art is publically showcased if it is approved")
    async def art_channel(self, interaction: discord.Interaction, submissions_channel: discord.TextChannel, showcase_channel: discord.TextChannel):
      await interaction.response.defer(ephemeral=True)
      try:
         if db.art.find_one({"guild_id": interaction.guild.id}):
              await interaction.followup.send(embed=embedutil("denied","The art module is already configured! Use /art set to manually set channels"))
              return

         if interaction.user.guild_permissions.manage_guild:
          if db.art.find_one({"guild_id": interaction.guild.id}):
            db.art.update_one({"guild_id": interaction.guild.id},{"$set": {"public_channel": showcase_channel.id,"submissions_channel":submissions_channel.id}})
          else:
            db.art.insert_one({"guild_id": interaction.guild.id,"public_channel": showcase_channel.id,"submissions_channel":submissions_channel.id})

          await submissions_channel.send(embed=embedutil("art","enabled_submissions"),view=requestedby(interaction.user))
          await showcase_channel.send(embed=embedutil("art","enabled_showcase"),view=requestedby(interaction.user))

          await interaction.followup.send(embed=embedutil("success",f"Successfully set {showcase_channel.mention} as the showcase channel and {submissions_channel.mention} as the submissions channel!"))
         else:
            await interaction.followup.send(embed=embedutil("denied","Your don't have permission to run this command"))
      except Exception:
            await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))


    @art_cmd.command(name="disable", description="Disable the art module")
    async def owslogs(self, interaction: discord.Interaction):
      await interaction.response.defer(ephemeral=True)
      try:

        if not interaction.permissions.manage_guild:
            await interaction.followup.send(embed=embedutil("denied","You don't have permissions to run this command!"),ephemeral=True)
            return

        if not db.art.find_one({"guild_id": interaction.guild.id}):
            await interaction.followup.send(embed=embedutil("denied","The art module is currently not configured yet!"),ephemeral=True)
            return

        for document in db.art.find({"guild_id": interaction.guild.id,}): 
              channel = self.bot.get_channel(document["public_channel"])
              await channel.send(embed=embedutil("art","disabled"),view=requestedby(interaction.user))
              db.art.delete_many({"guild_id": interaction.guild.id})
              db.art_submissions.delete_many({"guild_id": interaction.guild.id})
              await interaction.followup.send(embed=embedutil("success",f"Successfully disabled the art module"))
         
      except Exception:
         await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))


    @art_cmd.command(name="set",description="Manually set a channel after configuring if you need to change it")
    @app_commands.describe(type="If this channel should be set as the submissions channel or showcase channel!",channel="What channel to actually configure to be used as this")
    @app_commands.choices(type=[
      Choice(name="Submissions", value="submissions"),
      Choice(name="Showcase", value="showcase"),
    ])
    async def art_set(self, interaction: discord.Interaction, type: str, channel: discord.TextChannel):
      await interaction.response.defer(ephemeral=True)
      try:
         if not db.art.find_one({"guild_id": interaction.guild.id}):
              await interaction.followup.send(embed=embedutil("denied","The art module is currently not configured yet!"))
              return
         if not interaction.permissions.manage_guild:
            await interaction.response.send_message(embed=embedutil("denied","You don't have permissions to run this command!"),ephemeral=True)
            return

         if db.art.find_one({"guild_id": interaction.guild.id}):
            if type == "showcase":
               db.art.update_one({"guild_id": interaction.guild.id},{"$set": {"public_channel": channel.id}})
            elif type == "submissions":
               db.art.update_one({"guild_id": interaction.guild.id},{"$set": {"submissions_channel":channel.id}})

         await channel.send(embed=embedutil("art",f"enabled_{type}"),view=requestedby(interaction.user))
            

         await interaction.followup.send(embed=embedutil("success",f"Successfully set {channel.mention} as the {type} channel"))
      except Exception:
            await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))


    @art_cmd.command(name="submit",description="Submit a piece of art to be sent to the art channel!")
    @app_commands.describe(image="The art you want to submit, preferrably upload a .png, .jpeg or .jpg",name="What you want your art to be called",description="A simple description of what your art is about or whats in your art")
    async def submit_art(self, interaction: discord.Interaction, image: discord.Attachment, name: str, description: str):
        await interaction.response.defer(ephemeral=True)
        try:
          if not db.art.find_one({"guild_id": interaction.guild.id}):
              await interaction.followup.send(embed=embedutil("denied","The art module is currently not configured yet!"))
              return
          if db.art_submissions.count_documents({"art_author": interaction.user.id,"guild_id":interaction.guild.id}) == 2:
              await interaction.followup.send(embed=embedutil("denied","You have reached the limit on how many art submissions you can have open at once on this server! (2)"),ephemeral=True)
              return

          embed = discord.Embed(colour=0x4c7fff, title=name, description=description)
          embed.set_footer(text="Submitted by " + interaction.user.name.capitalize(), icon_url=interaction.user.avatar)
          embed.set_image(url=image.url)

          for document in db.art.find({"guild_id": interaction.guild.id}):
             submissions_channel = await self.bot.fetch_channel(document["submissions_channel"])
          submission_message = await submissions_channel.send(embed=embed,view=submission_buttons())

          await interaction.followup.send(embed=embedutil("success","Successfully submitted your art for review"))
          db.art_submissions.insert_one({"guild_id": interaction.guild.id,"message_id":submission_message.id,"image_url":image.url,"art_name":name,"art_description":description,"art_author":interaction.user.id})

          try:  
            await interaction.user.send(embed=embedutil("simple","You will recieve a dm from me when your art submission is either approved or denied, if you want to setup the Cloudy art module on your own server [click here](https://top.gg/bot/1090917174991933540)"))
          except:
             await interaction.followup.send(embedutil("simple","I was unable to send you a dm, please open your dms on this server so I can dm you when your art is either approved or denied"))
        except Exception:
           await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))




async def setup(bot):
    await bot.add_cog(art(bot))
