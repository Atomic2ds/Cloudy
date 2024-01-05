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

from functions.core import requestedby

# -- Processing one word stories --
async def process_ows(msg):
    cursor = client.fun.ows.find({"channel_id": msg.channel.id,})
    for document in cursor:
        try:
          last_author = document["last_author"]
        except:
          last_author = None
        if document["guild_id"] == msg.guild.id and document["channel_id"] == msg.channel.id and msg.author.bot == False:
            
            try:
                words = []
                story_words = document["words"]
                for item in story_words:
                 words.append(item)
                 words.append(" ")
                old_story = "".join(words)
                words.append(msg.content)
                words.append(" ")
                words = "".join(words)
                
            except:
              pass

            if len(msg.content) > 45:
              await msg.delete()
              try:
                  channel_id = document["log_id"]
                  channel = bot.get_channel(channel_id)
                  em = embedutil("ows",("log",msg.content,msg.author.name.capitalize(),msg.author.avatar,msg.guild.name,"Message was over the 45 character limit"))
                  await channel.send(embed=em,view=infoview("Automated message"))
              except:
                  await channel.send(embed=embedutil("error",traceback.format_exc()))

            if (any(not character.isalnum() for character in msg.content)):
                await msg.delete()
                try:
                  channel_id = document["log_id"]
                  channel = bot.get_channel(channel_id)
                  em = embedutil("ows",("log",msg.content,msg.author.name.capitalize(),msg.author.avatar,msg.guild.name,"Message contained non alpha-numeric characters!"))
                  await channel.send(embed=em,view=infoview("Automated message"))
                except:
                  await channel.send(embed=embedutil("error",traceback.format_exc()))
            elif last_author is not None and msg.author.id == last_author:
                await msg.delete()
                try:
                  channel_id = document["log_id"]
                  channel = bot.get_channel(channel_id)
                  em = embedutil("ows",("log",msg.content,msg.author.name.capitalize(),msg.author.avatar,msg.guild.name,"User can not send 2 messages in a row in community stories"))
                  await channel.send(embed=em,view=infoview("Automated message"))
                except:
                  await channel.send(embed=embedutil("error",traceback.format_exc()))


            
            elif len(words) > 4096:
              await msg.add_reaction("❌")
              await msg.channel.send(embed=embedutil("ows","limit"))
              return


            else:
                await msg.add_reaction("☑")
                client.fun.ows.update_one({"guild_id": msg.guild.id},{"$set": {"last_author": msg.author.id}})
                if client.fun.ows.find_one({"guild_id": msg.guild.id}):
                  client.fun.ows.update_one({ "guild_id": msg.guild.id },{ "$push": { "words": msg.content } })

                if len(old_story) < 2048 and len(words) > 2048:
                 await msg.channel.send(embed=embedutil("ows","halfway-warning"),view=infoview("Automated message"))

                if len(old_story) < 4000 and len(words) > 4000:
                 await msg.channel.send(embed=embedutil("ows","nearly-at-limit"),view=infoview("Automated message"))


# -- Publishing one word stories -- 
async def publish_story(interaction, name, info, db, bot=config.bot):
      await interaction.response.defer()
      try:
       
       if not db.ows.find_one({"guild_id": interaction.guild.id}):
          await interaction.followup.send(embed=embedutil("denied","The one word story is currently not configured yet!"),view=requestedby(interaction.user))
          return
       
       if not interaction.user.guild_permissions.manage_guild:
          await interaction.followup.send(embed=embedutil("denied","You require the manage server permission"), ephemeral=True,view=requestedby(interaction.user))
          return
       
       if len(name) > 256:
          await interaction.followup.send(embed=embedutil("denied","Story names can only be a max of 256 characters!"), ephemeral=True,view=requestedby(interaction.user))
          return
       
       if len(info) > 1024:
          await interaction.followup.send(embed=embedutil("denied","Story descriptions can only be a max of 1024 chracters!"), ephemeral=True,view=requestedby(interaction.user))
          return
       
       test = db.ows_stories.find_one({ "name": name, "guild_id": interaction.guild.id})
       if test:
          await interaction.followup.send(embed=embedutil("denied","Story name already exists on the library!"),view=requestedby(interaction.user))
          return

       guild_id = interaction.guild.id
       query = {"guild_id": guild_id}
       result = db.ows.find_one(query)
       if result:
          words = result["words"]
       else:
          await interaction.followup.send(embed=embedutil("denied","Unable to fetch the words from your story"), ephemeral=True,view=requestedby(interaction.user))
          return
       db.ows_stories.insert_one({"guild_id": interaction.guild.id,"name": name,"info": info, "words": words})
       try:
            cursor = client.fun.ows.find({"guild_id": interaction.guild.id,})
            db.ows.update_one({"guild_id": interaction.guild.id},{"$set": {"words": []}})
            db.ows.update_one({"guild_id": interaction.guild.id},{"$set": {"last_author": None}})
       except Exception as e:
           await interaction.followup.send(embed=embedutil("error",traceback.format_exc()), ephemeral=True,view=requestedby(interaction.user))
           print(e)
       query = {"guild_id": interaction.guild.id}
       results = db.ows.find(query)
       for result in results:
          channel = bot.get_channel(result["channel_id"])
          await channel.send(embed=embedutil("ows","published"),view=requestedby(interaction.user))
       await interaction.followup.send(embed=embedutil("success","Successfully uploaded your story to your servers story library!"),view=requestedby(interaction.user))
      except Exception:
         await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),view=requestedby(interaction.user))

# -- Resetting the one word story -- 
async def reset_ows(interaction, db, bot=config.bot):
     await interaction.response.defer()
     try:
         if interaction.user.guild_permissions.manage_guild:
            if not db.ows.find_one({"guild_id": interaction.guild.id}):
              await interaction.followup.send(embed=embedutil("denied","The one word story is currently not configured yet!"),view=requestedby(interaction.user))
              return
         
            cursor = client.fun.ows.find({"guild_id": interaction.guild.id,})
            db.ows.update_one({"guild_id": interaction.guild.id},{"$set": {"words": []}})
            db.ows.update_one({"guild_id": interaction.guild.id},{"$set": {"last_author": None}})
            await interaction.followup.send(embed=embedutil("success","Successfully Reset the current one word story"),view=requestedby(interaction.user))
            cursor = client.fun.ows.find({"guild_id": interaction.guild.id,})
            for document in cursor:
                channel = bot.get_channel(document["channel_id"])
                await channel.send(embed=embedutil("ows","reset"),view=requestedby(interaction.user))
         else:
           await interaction.followup.send(embed=embedutil("denied","You don't have permission to use this command"),view=requestedby(interaction.user))
     except Exception:
          await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),view=requestedby(interaction.user))


# -- Deleting a one word story -- 
async def delete_story(interaction, name, db, bot=config.bot):
     await interaction.response.defer()
     try:
         if interaction.user.guild_permissions.manage_guild:
            if not db.ows.find_one({"guild_id": interaction.guild.id}):
              await interaction.followup.send(embed=embedutil("denied","The one word story is currently not configured yet!"),view=requestedby(interaction.user))
              return
         
            db.ows_stories.delete_one({"guild_id": interaction.guild.id,"name": name})
            await interaction.followup.send(embed=embedutil("success","Successfully deleted your requested story!"),view=requestedby(interaction.user))
         else:
           await interaction.followup.send(embed=embedutil("denied","You don't have permission to use this command"),view=requestedby(interaction.user))
     except Exception:
          await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),view=requestedby(interaction.user))

# -- Reading a one word story -- 
async def read_story(interaction, name, db, bot=config.bot):
       await interaction.response.defer()
       try:
          if not db.ows.find_one({"guild_id": interaction.guild.id}):
            await interaction.followup.send(embed=embedutil("denied","The one word story is currently not configured yet!"))
            return
          
          guild_id = interaction.guild.id
          query = {"guild_id": guild_id, "name": name}
          results = db.ows_stories.find(query)
          for result in results:
            story_name = result["name"]
            story_info = result["info"]
            story_words = result["words"]
            words = []
            for item in story_words:
               words.append(item)
               words.append(" ")
            words = "".join(words)
            em = discord.Embed(colour=0x4c7fff, title=story_name, description=words)
            em.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)
          try: 
            await interaction.followup.send(embed=em,view=requestedby(interaction.user))
          except:
            await interaction.followup.send(embed=embedutil("denied",f"Unable to find a story named {name}"),ephemeral=True,view=requestedby(interaction.user))
       except Exception as e:
         await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),ephemeral=True,view=requestedby(interaction.user))

