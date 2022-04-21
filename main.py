import discord
import json
import http.client, urllib.request, urllib.parse, urllib.error, base64
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
import modules.commands as commandmodule

client = Bot(command_prefix='!')
slash = SlashCommand(client, sync_commands=True)

with open("config.json") as jsonfile:
    config = json.load(jsonfile)
    print('\033[1;32mConfig loaded')

@client.event
async def on_ready():
    print('\033[92mLoading data... \n \033[94mLoaded client: {0.user}'.format(client))
    import database.__init__ as db
    db.create_tables(config)
    print('\033[92mLoaded database')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"ov-NL"))


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

client.run(config['token'])