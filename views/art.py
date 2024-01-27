import discord
from discord import ui
from config import client
import traceback
from embeds import embedutil
global bot
from config import bot
from functions.core import infoview

db = client.fun


class submission_buttons(discord.ui.View):
  def __init__(self):
     super().__init__(timeout=None)

  @discord.ui.button(style=discord.ButtonStyle.gray, custom_id="approve_submission", emoji="<:cloudy_tick:1200839792968077332>")
  async def approvesubmission(self, interaction: discord.Interaction, button: discord.ui.Button):
    await interaction.response.defer()
    try:
     if not interaction.permissions.manage_guild:
        await interaction.response.send_message(embed=embedutil("denied","You don't have permissions to run this command!"),ephemeral=True)
        return
     
     if not db.art.find_one({"guild_id": interaction.guild.id}):
        await interaction.followup.send(embed=embedutil("denied","The art module is currently not configured yet!"))
        return

     for document in db.art_submissions.find({"message_id": interaction.message.id}):
        name = document["art_name"]
        description = document["art_description"]
        image_url = document["image_url"]

        author = bot.get_user(document["art_author"])
        embed = discord.Embed(colour=0x4c7fff, title=name, description=description)
        embed.set_footer(text="Submitted by " + author.name.capitalize(), icon_url=author.avatar)
        embed.set_image(url=image_url)

        for document in db.art.find({"guild_id": interaction.guild.id}):
          public_channel = await bot.fetch_channel(document["public_channel"])
        thread_msg = await public_channel.send(embed=embed)
        await public_channel.create_thread(name=f"Comments on {name}",type=discord.ChannelType.public_thread,message=thread_msg)

        await interaction.message.edit(view=infoview(f"Approved by {interaction.user.name.capitalize()}"))
        try:
          await author.send(embed=embedutil("simple",f"You art has been approved on {interaction.guild.name}! View it here: {thread_msg.jump_url}"))
        except:
          pass
        db.art_submissions.delete_many({"message_id": interaction.message.id})



    except Exception:
      await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))
  
  @discord.ui.button(style=discord.ButtonStyle.gray, custom_id="deny_submission", emoji="<:cloudy_cross:1200839806142394498>")
  async def denysubmission(self, interaction: discord.Interaction, button: discord.ui.Button):
    await interaction.response.defer()
    try:

        if not interaction.permissions.manage_guild:
            await interaction.response.send_message(embed=embedutil("denied","You don't have permissions to run this command!"),ephemeral=True)
            return
        
        if not db.art.find_one({"guild_id": interaction.guild.id}):
          await interaction.followup.send(embed=embedutil("denied","The art module is currently not configured yet!"))
          return

        await interaction.message.edit(view=infoview(f"Denied by {interaction.user.name.capitalize()}"))
        db.art_submissions.delete_many({"message_id": interaction.message.id})
        for document in db.art_submissions.find({"message_id": interaction.message.id}):
          author = bot.get_user(document["art_author"])
        try:
          await author.send(embed=embedutil("simple",f"You art has been denied on {interaction.guild.name}"))
        except:
          pass

    except Exception:
      await interaction.followup.send(embed=embedutil("error",traceback.format_exc()))