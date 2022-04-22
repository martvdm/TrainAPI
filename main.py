import discord
import json
import http.client, urllib.request, urllib.parse, urllib.error, base64
from datetime import datetime
from discord.ext import commands
from discord.ext import tasks
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
import modules.commands as commandmodule
import asyncio

client = commands.Bot(command_prefix='!')
slash = SlashCommand(client, sync_commands=True)

with open("config.json") as jsonfile:
    config = json.load(jsonfile)
    print('\033[1;32mConfig loaded')


@client.event
async def on_ready():
    print('\033[92mLoading data... \n \033[94mLoaded client: {0.user}'.format(client))
    # import database.__init__ as db
    # db.create_tables(config)
    print('\033[92mLoaded database')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"ov-NL"))
    loops.start()

@tasks.loop(seconds=60)
async def loops():
    from modules.commands.notify import checknotifications
    await checknotifications(client, config)


@slash.slash(name="station", description="Get station information")
async def station(ctx, *, station):
    from modules.commands.station import index
    await index(ctx, station, config, client)


@slash.slash(name="departures", description="Get station departures")
async def departures(ctx, *, station):
    from modules.commands.station import departures
    await departures(ctx, station, config, client)


@slash.slash(name="trip", description="Manage trips.")
async def trip(ctx: SlashContext):
    from modules.commands.trip import index
    await index(ctx, config, client)


@slash.slash(name="random", description="Get random station from current station")
async def random(ctx, *, station):
    from modules.commands.random import index
    await index(ctx, config, client)


@slash.slash(name="notify", description="Get notifications from a station")
async def notify(ctx, *, station):
    from modules.commands.notify import index
    await index(ctx, station, config, client)


client.run(config['token'])
