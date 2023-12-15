import discord
from discord import ui
from functions import publish_story, reset_ows, delete_story, read_story

class publish_story_modal(ui.Modal, title="Publish Story"):
    story_name = ui.TextInput(label="Name of the story", placeholder="What you want to name your one word story", style=discord.TextStyle.short, required=True)
    story_info = ui.TextInput(label="Story Description", placeholder="Briefely describe the story in a short form", style=discord.TextStyle.long, required=True)

    async def on_submit(self, interaction: discord.Interaction):
     from cogs.ows import db
     name = str(self.story_name)
     info = str(self.story_info)
     await publish_story(interaction, name, info, db)

class compileview(discord.ui.View):
  def __init__(self):
     super().__init__(timeout=None)
     #self.add_item(discord.ui.Button(label=f"Requested by {self.username}",style=discord.ButtonStyle.gray, custom_id="balls", disabled=True))

  @discord.ui.button(label="Publish Story", style=discord.ButtonStyle.gray, custom_id="publish_story", emoji="📪")
  async def publishstory(self, interaction: discord.Interaction, button: discord.ui.Button):
     await interaction.response.send_modal(publish_story_modal())

  @discord.ui.button(label="Reset Story", style=discord.ButtonStyle.gray, custom_id="reset_story", emoji="🗑️")
  async def resetstory(self, interaction: discord.Interaction, button: discord.ui.Button):
    from cogs.ows import db
    await reset_ows(interaction, db)

class storiesview(discord.ui.View):
  def __init__(self):
     super().__init__(timeout=None)
     #self.add_item(discord.ui.Button(label=f"Requested by {self.username}",style=discord.ButtonStyle.gray, custom_id="balls", disabled=True))\


  @discord.ui.button(label="Delete Story", style=discord.ButtonStyle.gray, custom_id="delete_story", emoji="🗑️")
  async def deletestory(self, interaction: discord.Interaction, button: discord.ui.Button):
     await interaction.response.send_modal(delete_story_modal())

  @discord.ui.button(label="Read Story", style=discord.ButtonStyle.gray, custom_id="read_story", emoji="🌴")
  async def readstory(self, interaction: discord.Interaction, button: discord.ui.Button):
     await interaction.response.send_modal(read_story_modal())
  

class delete_story_modal(ui.Modal, title="Delete Story"):
    story_name = ui.TextInput(label="Name of the story", placeholder="The name of the story you want to delete", style=discord.TextStyle.short, required=True)

    async def on_submit(self, interaction: discord.Interaction):
     from cogs.ows import db
     name = str(self.story_name)
     await delete_story(interaction, name, db)

class read_story_modal(ui.Modal, title="Read Story"):
    story_name = ui.TextInput(label="Name of the story", placeholder="The name of the story you want to read", style=discord.TextStyle.short, required=True)

    async def on_submit(self, interaction: discord.Interaction):
     from cogs.ows import db
     name = str(self.story_name)
     await read_story(interaction, name, db)