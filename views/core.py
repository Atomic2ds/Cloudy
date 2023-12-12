import discord
from discord import ui

class helpdropdown(discord.ui.Select):
  def __init__(self):
    options=[
      discord.SelectOption(label="Overview",description="View all of the command modules", emoji="🏡"),
      discord.SelectOption(label="Core commands",description="Anything to do with the bot", emoji="🚀"),
      discord.SelectOption(label="Fun commands", description="Things you can goof around with", emoji="🎮"),
      discord.SelectOption(label="Utility commands",description="Used to improve your server",emoji="⚙️"),
      discord.SelectOption(label="Fact commands",description="Fact of the day channels and random facts",emoji="💡"),
      discord.SelectOption(label="Story commands",description="Setup your own one word story in your server",emoji="📘"),
      discord.SelectOption(label="Image commands",description="Manage your own text to image channel",emoji="📸"),
    ]

    super().__init__(placeholder="Choose a command type...", options=options, min_values=1, max_values=1, custom_id="helpdropdown")

  async def callback(self, interaction: discord.Interaction):
    from embeds import embedutil
    if self.values[0] == "Overview":
      await interaction.response.edit_message(embed=embedutil("help","overview"),view=helpoverview())
    if self.values[0] == "Fun commands":
      await interaction.response.edit_message(embed=embedutil("help","fun"),view=helpoverview())
    if self.values[0] == "Core commands":
      await interaction.response.edit_message(embed=embedutil("help","core"),view=helpoverview())
    if self.values[0] == "Duck commands":
      await interaction.response.edit_message(embed=embedutil("help","duck"),view=helpoverview())
    if self.values[0] == "Utility commands":
      await interaction.response.edit_message(embed=embedutil("help","utility"),view=helpoverview())
    if self.values[0] == "Fact commands":
      await interaction.response.edit_message(embed=embedutil("help","fact"),view=helpoverview())
    if self.values[0] == "Story commands":
      await interaction.response.edit_message(embed=embedutil("help","story"),view=helpoverview())
    if self.values[0] == "Image commands":
      await interaction.response.edit_message(embed=embedutil("help","image"),view=helpoverview())
  
class helpoverview(discord.ui.View):
   def __init__(self):
      super().__init__(timeout=None)
      self.add_item(helpdropdown())

class inviteview(discord.ui.View):
   def __init__(self):
      super().__init__(timeout=None)
      self.add_item(discord.ui.Button(label="Invite Donald!", url="https://donald.a3d.pro/invite"))

class voteview(discord.ui.View):
   def __init__(self):
      super().__init__(timeout=None)
      self.add_item(discord.ui.Button(label="Vote for Donald!", url="https://donald.a3d.pro/vote"))