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
                 await msg.channel.send(embed=embedutil("ows","halfway-warning"))

                if len(old_story) < 4000 and len(words) > 4000:
                 await msg.channel.send(embed=embedutil("ows","nearly-at-limit"))



async def handle_autoroles(member):
 if member.bot == False:
  try:
    cursor = client.utils.autoroles.find({"guild_id": member.guild.id,})
    for document in cursor:
      roles = document["human_roles"]
      for item in roles:
        role = discord.utils.get(member.guild.roles,id=item)
        await member.add_roles(role)
  except Exception:
    print(traceback.format_exc())
 if member.bot == True:
   try:
    cursor = client.utils.autoroles.find({"guild_id": member.guild.id,})
    for document in cursor:
      roles = document["bot_roles"]
      for item in roles:
        role = discord.utils.get(member.guild.roles,id=item)
        await member.add_roles(role)
   except Exception as e:
    print(traceback.format_exc())



async def process_img2text(msg):
  if msg.author.bot == False:
    cursor = client.images.config.find({"channel_id": msg.channel.id})
    for document in cursor:
       status = document["status"]
    if status:
       if status == "enabled":
        try:
          embed = await img2text(msg.content)
          await msg.reply(embed=embed, mention_author=False)
        except Exception:
          embed = embedutil("error",traceback.format_exc())
          await msg.reply(embed=embed,mention_author=False)

async def img2text(query):
    try:
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=15&page=1"
        headers = {"Authorization": config.PEXELS_API}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response_data = await response.json()

        embed = discord.Embed(colour=0x4c7fff, description=f"Prompt: {query}")
        embed.set_footer(text="Sourced from pexels.com")

        if "photos" in response_data:
            photos = response_data["photos"]
            if len(photos) > 0:
                embed.set_image(url=random.choice(photos)["src"]["original"])
                return embed
            
        embed = embedutil("simple", "Unable to find an image based on your query")
        return embed

    except Exception:
        return embedutil("error", traceback.format_exc())
    

async def get_avatar(user):
  pfp = user.avatar
  embed = discord.Embed(title="Avatar Viewer", colour=0x4c7fff)
  embed.set_image(url=str(pfp))
  return embed

async def fetch_gif(query):
  try:
   session = aiohttp.ClientSession()

   if query == None:
      response = await session.get(f'https://api.giphy.com/v1/gifs/random?api_key={config.GIPHY_KEY}')
      data = json.loads(await response.text())
      embed = embedutil("gif",(None,"Random Gif",data['data']['images']['original']['url']))

   else:
      search = query.replace(' ', '+')
      response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + f'&api_key={config.GIPHY_KEY}')
      data = json.loads(await response.text())
      gif_choice = random.randint(0, 9)
      embed = embedutil("gif",(query,"Custom Gif",data['data'][gif_choice]['images']['original']['url']))

   
  except Exception:
     embed = embedutil("error",traceback.format_exc())

  await session.close()
  return embed

async def define(term):
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    headers = {
      "X-RapidAPI-Key": "09efa8afd5msh469606e5298e21cp14d14ajsnfd148325b4b2"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params={"term": term}) as response:
            data = await response.json()

    if len(data["list"]) > 0:
        definition = data["list"][0]["definition"]
        return definition
    else:
        return "Sorry, I couldn't find a definition for that term."
    
async def get_definition(word):
  try:
    response = await define(word)
    embed=embedutil("definition",(word,response))
  except Exception:
    embed=embedutil("error",traceback.format_exc())
  
  return embed

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


class hyperlink_button(discord.ui.View):
   def __init__(self, link: str,label: str):
      super().__init__()
      self.inv = link
      self.label = label
      self.add_item(discord.ui.Button(label=self.label, url=self.inv))

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


class requestedby(discord.ui.View):
   def __init__(self, user: discord.User):
      super().__init__()
      self.user = user
      self.add_item(discord.ui.Button(label=f"Run by {self.user.name.capitalize()}",style=discord.ButtonStyle.gray, disabled=True))

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