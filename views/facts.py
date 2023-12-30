from discord import ui
from config import bot
import discord
import traceback
from embeds import embedutil


class factview(discord.ui.View):
  def __init__(self, username: str):
     super().__init__(timeout=None)
     self.username = username
     self.add_item(discord.ui.Button(label=f"Requested by {self.username}",style=discord.ButtonStyle.gray, custom_id="balls", disabled=True))

  @discord.ui.button(label="Send Another", style=discord.ButtonStyle.blurple, custom_id="another_fact", emoji="📫")
  async def sendanotherfact(self, interaction: discord.Interaction, button: discord.ui.Button):
      await interaction.response.defer()
      try:
        await interaction.followup.send(embed=embedutil("fact","Random Fact"),view=factview(interaction.user.name.capitalize()))
      except Exception:
         await interaction.followup.send(embed=embedutil("error",traceback.format_exc()),ephemeral=True)