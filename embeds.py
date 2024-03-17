import discord
from config import bot
import libraries
import traceback
import random
from config import client
import json
import requests

def embedutil(category, content):
  try:

    if category == "servers":
        if content == "status":
         embed = discord.Embed(colour=0x4c7fff, title="Server Linker Status",description="View the status of a server linked to your discord server by using the dropdown menu below")
         embed.add_field(name="Adding servers",value="You can add a server to this menu by using the /server add command, then you can enter a server id, panel url and api key",inline=False)
         embed.set_footer(text="This module is in beta, report any bugs to our support server")
         embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)
        elif content == "delete":
         embed = discord.Embed(colour=0x4c7fff, title="Linked Server Deleter",description="Select as many servers as you want from the dropdown menu below and we will remove them from your server list")
         embed.set_footer(text="This module is in beta, report any bugs to our support server")
         embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)
        elif content == "selectservers":
         embed = discord.Embed(colour=0x4c7fff, title="Select Servers",description="Choose servers to put on your server panel, using the dropdown menu below")
         embed.set_footer(text="This module is in beta, report any bugs to our support server")
         embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)

    if category == "smp":
        
        if content[1]  != None:
            title = content[1].replace("{guild_name}",content[0])
        else:
            title = f"SMP panel for {content[0]}"

        if content[2] != None:
            description = content[2].replace("{guild_name}",content[0])
        else:
            description="Click the buttons below to view information about the currently linked smp and also current running status and stats like cpu usage, memory usage and disk usage"

        embed = discord.Embed(colour=0x4c7fff, title=title, description=description)

    if category == "serverpanel":
        title = content[0]
        description = content[1]
        embed = discord.Embed(colour=0x4c7fff, title=title, description=description)

    if category == "img2text":
        query = content
    
    if category == "fact":
        limit = 1
        api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
        response = requests.get(api_url, headers={'X-Api-Key': '9060KEZGpC2iPBDBL2uIAQ==xCfeT1jCVGkrVkxz'})
        response_json = json.loads(response.text)
        if 'fact' in response_json[0]:
            response_fact = response_json[0]['fact']
        embed = discord.Embed(colour=0x4c7fff, title=content, description=response_fact)
        embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)

    if category == "basement":
        db = client.fun
        interaction = content[0]
        if content[1] == None:
            user = interaction.user
            content = "Use /basement add to add someone new to your basement"
            title = "Your Personal Basement"
        else:
            user = content[1]
            content = None
            title = f"{user.name}'s Basement"
        try:
            footer = interaction.guild.name
        except:
            footer = "Cloudy Bot"
        embed = discord.Embed(colour=0x4c7fff, title=title, description=content)
        embed.set_footer(text=footer)
        cursor = db.basements.find({'id': user.id})
        for document in cursor:
          name = document["name"]
          description = document["description"]
          embed.add_field(name=name, value=description)


    if category == "definition":
        embed = discord.Embed(colour=0x4c7fff, title=f"Definition of {content[0]}",description=content[1])
        embed.set_footer(text="We did not write these definitions")

    if category == "art":
        if content == "enabled_submissions":
            embed = discord.Embed(colour=0x4c7fff, title="Submissions channel set", description="This is the place where staff will approve or deny art submissions, we recommend making this channel private")
            embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)
        if content == "enabled_showcase":
            embed = discord.Embed(colour=0x4c7fff, title="Showcase channel set", description="Members can now apply to have their art posted and featured on this channel, use the command /art apply to apply to have your art posted")
            embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)
        if content == "disabled":
            embed = discord.Embed(colour=0x4c7fff, title="Public Notice", description="This channel no longer functions properly because the Cloudy art module has been disabled and all content has been cleared from our systems")
            embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)


    if category == "ows":
        if content == "reset":
            embed = discord.Embed(colour=0x4c7fff, title="Story has been reset!", description="The story has been reset, all of the words in the story have been cleared out of the cache")
            embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)
        elif content[0] == "welcome":
            embed = discord.Embed(colour=0x4c7fff, title="Welcome to the One Word Story!", description="This channel has been configured as the one word story channel, you can't send more than 1 message in a row and you can't have more than 1 word in a message")
            embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)
        elif content[0] == "disabled":
            embed = discord.Embed(colour=0x4c7fff, title="One word story disabled", description="The one word story channel has been disabled and has been reset, all data has been cleared from our system")
            embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)
        elif content[0] == "log":
            embed = discord.Embed(colour=0x4c7fff, title=f"Message Deleted in one word stories",description=content[1])
            embed.add_field(name="Deletion Reason", value=content[5])
            embed.set_author(name=f"Original Message by {content[2]}" , icon_url=content[3])
            embed.set_footer(text=content[4])
        elif content[0] == "logs set":
            embed = discord.Embed(colour=0x4c7fff, title=f"Logs channel set",description="This channel has been configured as the logs channel for one word stories")
            embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)
        elif content[0] == "compile":
            embed = discord.Embed(colour=0x4c7fff, title="Your one word story", description=content[1])
            embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)
        elif content == "published":
            embed = discord.Embed(colour=0x4c7fff, title="One word story published", description="The previous story has been published to your servers library, the story in this channel has been automatically reset")
            embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)
        elif content == "limit":
            embed = discord.Embed(colour=0x4c7fff, title="Length Limit", description="That word will take your story over the 4096 chracter limit (Discords embed description limit) Either publish/reset your story or send a different word")
            embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)
        elif content == "halfway-warning":
            embed = discord.Embed(colour=0x4c7fff, title="Length warning", description="You have gone over the halfway mark on how long your story can be, think about publishing/restting it soon")
            embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)
        elif content == "nearly-at-limit":
            embed = discord.Embed(colour=0x4c7fff, title="Length warning", description="You are 96 characters off the one word story character limit, you should REALLY think about publishing/restting your story")
            embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)
        elif content[0] == "purged":
            embed = discord.Embed(colour=0x4c7fff, title="Channel Purged", description=f"The one word story channel was just purged having {content[1]} message(s) purged from the channel and the story, if anything is missing thats why")
            embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)

    if category == "quotes":
        if content == "configured":
            embed = discord.Embed(colour=0x4c7fff, title="Quotes channel has been configured", description=f"This channel has been set as the place for saved quotes to be sent, you can save a quote by right clicking a message then going to apps. After that click on 'Save As Quote' then it will be sent to this channel. Have fun with it!")
            embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)


    if category == "8ball":
        embed = discord.Embed(colour=0x4c7fff, title="Magic 8 Ball")
        embed.add_field(inline=False,name="Question",value=f"{content}")
        eight_ball_answers = ("Yes, definitely.", "No, never.", "Ask again later.", "Cannot predict now.", "Don't count on it.", "Most likely.", "Outlook not so good.", "Reply hazy, try again.")
        embed.add_field(inline=False,name="Answer",value=f"{random.choice(eight_ball_answers)}")

    if category == "invite":
        embed = discord.Embed(colour=0x4c7fff, description=f"Click the button below to invite Cloudy bot to your own discord server!", title="Invite Link")

    if category == "vote":
        embed = discord.Embed(colour=0x4c7fff, description=f"Click the button below to vote for Cloudy on top.gg and make it easier for more people to find us!", title="Vote Link")

    if category == "support":
        embed = discord.Embed(colour=0x4c7fff, description=f"Click the button below to join the Cloudy support server, here you can report bugs, suggest new features and much more", title="Support Server")

    if category == "documentation":
        embed = discord.Embed(colour=0x4c7fff, description=f"Click the button below to view our documentation and learn how to setup different modules on the bot", title="Documentation Link")

    if category == "faq":
        embed = discord.Embed(colour=0x4c7fff, description=f"Below are some frequently asked questions about Cloudy",title="Cloudy FAQ")
        embed.add_field(inline=False,name="How is Cloudy hosted",value="We use a virtual private server located in Germany so we can have good specs while the bot is still extremely cheap to run")
        embed.add_field(inline=False,name="How can I trust Cloudy won't raid or destroy my server?",value="All of our servers are secure and encrypted, if we raided or destroyed your server our accounts would get terminated from discord, also top.gg has to verify and test all bots they add to their website and if the bot raided their testing server we wouldn't be on top.gg")
        embed.add_field(inline=False,name="Will Cloudy always be 100% free", value="Most likely not, I have to pay quite a bit for the infrastructure to host the bot. However I will keep limits high but offer extensions to limits if you buy premium like I will let you have 8000 or 16000 characters in your one word story instead of 4096")
        embed.add_field(inline=False,name="Are all features on Cloudy tested?",value="Yes, we have 2 testing bots so we can have 2 people working on the bot at once, we also have our own database server for testing features so nothing can get destroyed")
        embed.add_field(inline=False,name="Do you take backups of your infrastructure",value="Absolutely, we take daily backups of our database server and our bot is on github, our database backups go back 5 days")
        embed.add_field(inline=False,name="Social Links",value=libraries.SOCIAL_LINKS)

    if category == "gif":
        embed = discord.Embed(colour=0x4c7fff, title=content[1],description=content[0])
        embed.set_image(url=content[2])
        embed.set_footer(text="Sourced from Giphy")

    if category == "core":
        if content == "ping":
            embed = discord.Embed(colour=0x4c7fff, description=f"Pong! Connnections take {round(bot.latency * 1000)}ms")

        elif content == "about":
            embed = discord.Embed(colour=0x4c7fff, description="We built cloudy so that server owners could easily add fun and cool features to their server without compromising on simplicity. Cloudy is made to be fast and responsive while being packed with cool and unique features",title="About Cloudy Bot")
            embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)

        elif content[0] == "update":
            title = content[1]
            description = content[2]
            interaction = content[3]
            embed = discord.Embed(title=title, description=description, colour=0x4c7fff)
            embed.set_author(name=interaction.user.name.capitalize() + "・Bot Developer", icon_url=interaction.user.avatar)
            embed.set_footer(text=interaction.guild.name)

    if category == "warning":
        if content == "dms":
            embed = discord.Embed(colour=0x4c7fff,description=f"⚠️ Currently a lot of commands are broken in dms, we do not recommend running stuff here, you should make a testing server instead")
        else:
           embed = discord.Embed(colour=0x4c7fff,description=f"⚠️ Warning: {content}")

    if category == "error":
        embed = discord.Embed(colour=0x4c7fff,description=f"Uh oh! An error occured, thankfully it was caught by our handler. If this error continues report it to our support server```{content}```")

    if category == "simple":
        embed = discord.Embed(colour=0x4c7fff,description=content)

    if category == "denied":
        embed = discord.Embed(colour=0xff3939,description=f"<:offline:1078291224840114186> {content}")

    if category == "success":
        embed = discord.Embed(colour=0x1fff8b,description=f"<:online:1078291279756136488>  {content}")
    
    if category == "help":
        if content == "overview":
            embed = discord.Embed(colour=0x4c7fff,title="Modules on Cloudy",description="Welcome to Cloudy, below are commands and modules you can play with!")
            embed.add_field(name="🚀 Core commands", value="Commands about the bot, like about the ping, the bots ping, stuff like that")
            embed.add_field(name="🎳 Fun commands", value="Play around with things like memes from reddit, gifs and the magic 8 ball")
            embed.add_field(name="⚙️ Utility commands", value="Do things like make polls, set custom slowmode, get peoples avatatrs, send warnings and more")
            embed.add_field(name="💡 Fact commands", value="Set your own fact of the day channel, and get random facts quickly")
            embed.add_field(name="📘 Story commands", value="Setup and run your own one word story channel, highly flexible and packed with features")
            embed.add_field(name="📸 Image commands", value="Setup your own image to text channel, automatically converts all messages sent to images")
            embed.add_field(name="🎮 SMP commands", value="Connect your minecraft smp server to your discord community and let your members view the status and basic info")

        elif content == "fun":
            embed = discord.Embed(colour=0x4c7fff,title="Fun commands",description="These are just commands to goof around with")
            embed.add_field(name="/meme", value="Get a meme from reddit, you can choose from 7 different subreddits")
            embed.add_field(name="/gif", value="Fetch a gif from giphy, with support for custom search querys")
            embed.add_field(name="/8ball", value="Ask a question to the magic 8 ball and get its response")
            embed.add_field(name="/template", value="Put anyones profile picture onto a image template")
            embed.add_field(name="/basement view", value="View everyone you have added to your basement")
            embed.add_field(name="/basement add", value="Add someone new to your basement with a name and description")
            embed.add_field(name="/basement remove", value="Remove someone from your basement with their name")

        elif content == "core":
            embed = discord.Embed(colour=0x4c7fff,title="Core commands",description="Any commands associated with the bot")
            embed.add_field(name="/about", value="View information about the bot, and get the invite link and support server")
            embed.add_field(name="/ping", value="Check the ping from our server to discord api, also a health check")
            embed.add_field(name="/help", value="What your using right now, view all commands available on the bot")
            embed.add_field(name="/vote", value="Vote for the Cloudy bot on top.gg, to help us climb the leaderboards")
            embed.add_field(name="/invite", value="Get a link to invite the bot to your own discord server community")
            embed.add_field(name="/support", value="Join our support server to suggest features, report bugs and more!")
        
        elif content == "duck":
            embed = discord.Embed(colour=0x4c7fff,title="Duck commands",description="Commands to do with ducks because we love ducks")
            embed.add_field(name="/duck", value="Get an image or imgur post related to a duck, very fun to spam")

        elif content == "utility":
            embed = discord.Embed(colour=0x4c7fff,title="Utility commands",description="Simple utilities you can use to improve your server")
            embed.add_field(name="/warning", value="Send a warning to chat, I have no ideawhat the point of this is")
            embed.add_field(name="/slowmode", value="Set a custom slowmode on a channel, useful for if you want a 1s or 2s slowmode")
            embed.add_field(name="/echo", value="Send a message as the bot iself, nothing is linked back to you")
            embed.add_field(name="/poll", value="Make either a simple poll with a yes/no answer or a custom poll with custom options")
            embed.add_field(name="/avatar", value="Get your avatar or any users avatar and see it up close, with a link to it")
            embed.add_field(name="/define", value="Get the definition of any word, just for your information we did not write these")

        elif content == "fact":
            embed = discord.Embed(colour=0x4c7fff,title="Fact commands",description="Set a fact of the day channel or just get a random fact")
            embed.add_field(name="/fact random", value="Grab a random fact from the same api we use the fact of the days")
            embed.add_field(name="/fact channel", value="Set a channel for a fact to be sent to every single day")
            embed.add_field(name="/fact disable", value="Disable the fact of the day channel, resetting the configuration")
            embed.add_field(name="/fact trigger", value="Can only be used by bot devs, triggers a fotd bypassing the schedule")

        elif content == "story":
            embed = discord.Embed(colour=0x4c7fff,title="Story commands",description="Help with setting up your own one word story channel on your community")
            embed.add_field(name="/ows channel", value="Sets up the module, configure a channel for your story")
            embed.add_field(name="/ows logs", value="Configure a channel for where automated message deletions will go")
            embed.add_field(name="/ows disable", value="Disable the entire module and clear all data related to this module")
            embed.add_field(name="/ows reset", value="Reset the story on your server, see the next command as a better way of handling this")
            embed.add_field(name="/ows publish", value="Publish your story to your servers story library, this is not public")
            embed.add_field(name="/ows read", value="Read a story from your servers story library, anyone can use this")
            embed.add_field(name="/ows reset", value="Reset the story on your server, see the next command as a better way of handling this")
            embed.add_field(name="/ows compile", value="Turn the list of words from your story into a nice readable paragraph")
            embed.add_field(name="/ows delete", value="Delete a story from your servers story library")

        elif content == "image":
            embed = discord.Embed(colour=0x4c7fff,title="Image commands",description="Run and manaage your own text to image channel in your server")
            embed.add_field(name="/image channel", value="Sets up the module, set the image to ")
            embed.add_field(name="/image disable", value="Disable the text to image channel, requires the channel to be set")
            embed.add_field(name="/image enable", value="Enable the text to image channel after disabling it")

        elif content == "smp":
            embed = discord.Embed(colour=0x4c7fff,title="SMP commands",description="Connect your minecraft smp server to your discord community easily")
            embed.add_field(name="/smp link", value="Link an smp to your discord server, only 1 can be linked at a time")
            embed.add_field(name="/smp unlink", value="Disconnect your smp from your discord community, this lets you link a different server")
            embed.add_field(name="/smp info", value="Information like limits on things such as cpu thread limit, database limit, cpu limit, memory limit, etc")
            embed.add_field(name="/smp status", value="View detailed stats about your smp server, showing things like CPU, RAM, Disk Space, Network Traffic and more")

    if category == "meme":
        embed = discord.Embed(colour=0x4c7fff, title="Random Meme")
        embed.set_image(url=content[0])
        embed.set_footer(text=f"Fetched from r/{content[1]}")

    elif category == "welcome":
        if content == "message":
          embed = discord.Embed(title="Thanks for adding Cloudy Bot",colour=0x4c7fff,description="Below you can see basic tutorials on how to setup some of our features")
          embed.add_field(name="One word stories",value="A feature rich system for making one word stories with your server members, fast and responsive with things like publishing, compiling, purging, invalid character detection and more. Get started with </ows channel:1097919110249185390>",inline=False)
          embed.add_field(name="Link your SMP", value="Connect your minecraft smp server to your discord community easily and view things like its current running state, resource usage and extras like resource limits for example how many databases you can have, start off with </smp link:1192840039638507603>", inline=False)
          embed.add_field(name="Text to image channels", value="You can setup a text to image channel so that any message sent into that channel you set is automatically prompted to an image website and it sends that image back, set it up with </image channel:1180400850275946564>",inline=False)
          embed.add_field(name="Social Links",value=libraries.SOCIAL_LINKS,inline=False)
          em = embed

    return embed

  except Exception:
      embed = embedutil("error",traceback.format_exc())
      return embed
