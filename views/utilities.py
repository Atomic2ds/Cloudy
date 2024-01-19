import discord
from discord import ui
from embeds import embedutil
import traceback
from functions.core import infoview

class avatarview(discord.ui.View):
   def __init__(self, user: str):
      super().__init__()
      self.user = user
      self.add_item(discord.ui.Button(label="Avatar URL", url=f"{self.user.avatar}"))
      self.add_item(discord.ui.Button(label=f"{self.user.name.capitalize()}'s Avatar",style=discord.ButtonStyle.gray, disabled=True))

class create_embed(ui.Modal, title="Create Embed"):
    embed_title = ui.TextInput(label="Embed Title", placeholder="What you want the name of the embed to be", style=discord.TextStyle.short, required=False)
    embed_description = ui.TextInput(label="Embed Description", placeholder="What you want the embed description to be", style=discord.TextStyle.long, required=False)
    embed_footer = ui.TextInput(label="Embed Footer", placeholder="What you want the embed footer to be", style=discord.TextStyle.short, required=False)
    embed_image = ui.TextInput(label="Embed Image", placeholder="What you want the embed image to be", style=discord.TextStyle.short, required=False)
    embed_thumbnail = ui.TextInput(label="Embed Thumbnail", placeholder="What you want the embed thumbnail to be", style=discord.TextStyle.short, required=False)

    async def on_submit(self, interaction: discord.Interaction):
     try:

      embed = discord.Embed(colour=0x4c7fff, title=self.embed_title, description=self.embed_description)
      embed.set_author(name=interaction.user.name.capitalize(),icon_url=interaction.user.avatar)
      if not self.embed_footer == None:
         embed.set_footer(text=self.embed_footer)
      if not self.embed_image == None:
         embed.set_image(url=self.embed_image)
      if not self.embed_thumbnail == None:
         embed.set_thumbnail(url=self.embed_thumbnail)

      await interaction.channel.send(embed=embed)
      await interaction.response.send_message(embed=embedutil("success",f"Successfully sent your embed to {interaction.channel.mention}"),ephemeral=True)


     except Exception:
       await interaction.response.send_message(embed=embedutil("error",traceback.format_exc()),ephemeral=True)