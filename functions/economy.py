import random


broke_messages = ("Get a job bruh","No like actually get a job","Why don't you sell someone in your basement","You're more broke than Atomic")

def balance_quotes(balance):
    if balance == 0:
        return random.choice(broke_messages)