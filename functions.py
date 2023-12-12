from config import client, bot
import discord
import random
from embeds import embedutil
import traceback
import requests
import config
import aiohttp
import asyncio

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
                  await channel.send(embed=em)
              except:
                  pass

            if (any(not character.isalnum() for character in msg.content)):
                await msg.delete()
                try:
                  channel_id = document["log_id"]
                  channel = bot.get_channel(channel_id)
                  em = embedutil("ows",("log",msg.content,msg.author.name.capitalize(),msg.author.avatar,msg.guild.name,"Message contained non alpha-numeric characters!"))
                  await channel.send(embed=em)
                except:
                  pass
            elif last_author is not None and msg.author.id == last_author:
                await msg.delete()
                try:
                  channel_id = document["log_id"]
                  channel = bot.get_channel(channel_id)
                  em = embedutil("ows",("log",msg.content,msg.author.name.capitalize(),msg.author.avatar,msg.guild.name,"User can not send 2 messages in a row in community stories"))
                  await channel.send(embed=em)
                except:
                  pass


            
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