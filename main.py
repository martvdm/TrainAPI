import discord
from discord.ext import tasks, commands
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext

client = commands.Bot(command_prefix='!')
slash = SlashCommand(client)

import json
with open("config.json") as jsonfile:
    config = json.load(jsonfile)

@client.event
async def on_ready():
    print('\033[92mLoading data... \n \033[94mLoaded client: {0.user}'.format(client))
    print('\033[92mLoading commands...')
    print('\033[92mLoaded commands!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"ov-NL"))

@slash.slash(name="test")
async def test(ctx: SlashContext):
    await ctx.send("test")

client.run(config['token'])