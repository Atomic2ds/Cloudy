# Cloudy Bot
My attempt at building a sleek, responsive and feature packed multipurpose discord bot

## Links
- ### [🚀 Project Tracker](https://trello.com/b/ED1yTBL0/cloudy-bot): Includes ideas, to-do, in progress, on hold and completed
- ### [🌏 Top.gg Page](https://top.gg/bot/1090917174991933540): The page to add Cloudy to your server, vote for it & more
- ### [🆘 Support Server](https://discord.gg/Gn2YbxQsgs): Talk to us here! Suggest things and tell us how we can improve
- ### [➕ Invite Link](https://top.gg/bot/1090917174991933540/invite): The link to add Cloudy to your discord server


## Deploying the stack
I use docker & docker compose primarily for ease of use, you are free to use pretty much whatever you want
### Setting up the environment
  ```
  git clone https://github.com/Atomic2ds/Cloudy && cd Cloudy
  ```
Clone the repository, then you need to open a terminal window in the repository folder

### Environment Variables
You need to make a .env file for deploying the bot, copy it over from .env.example
  ```
  cp .env.example .env
  ```
Now simply just edit the 2 variables set, make sure to set TOKEN to your bot token


### Deploying the stack
Make sure you have docker installed, docker is supported on pretty much every os including macos, windows and linux
  ```
  docker-compose up -d
  ```
Running that command will install the dependencies, create the containers, networks and volumes required. 

