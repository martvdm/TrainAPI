import discord



client = discord.Client()

import json
with open("config.json") as jsonfile:
    config = json.load(jsonfile)

@client.event
async def on_ready():
    print('\033[92mLoading data... \n \033[94mLoaded client: {0.user}'.format(client))



client.run(config['token'])