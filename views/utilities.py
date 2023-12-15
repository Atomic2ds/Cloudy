import discord

class avatarview(discord.ui.View):
   def __init__(self, user: str):
      super().__init__()
      self.user = user
      self.add_item(discord.ui.Button(label="Avatar URL", url=f"{self.user.avatar}"))
      self.add_item(discord.ui.Button(label=f"{self.user.name.capitalize()}'s Avatar",style=discord.ButtonStyle.gray, disabled=True))