# About Cloudy
A small multipurpose discord bot that I sometimes work on when im bored, it is hosted publically and everything on the bot is 100% free to use

# Deploying the stack
Clone the repository, then you need to open a terminal window in the repository folder
```
git clone https://github.com/Atomic2ds/Cloudy && cd Cloudy
```
You need to make a .env file for deploying the bot, copy it over from .env.example
```
cp .env.example .env
```
Make sure you have docker installed, docker is supported on pretty much every os including macos, windows and linux
```
docker-compose up -d
```
Running that command will install the dependencies, create the containers, networks and volumes required. 
