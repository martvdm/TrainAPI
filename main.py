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
import yaml

client = commands.Bot(command_prefix='!')
slash = SlashCommand(client, sync_commands=True)

with open('config.yaml') as file:
    config = yaml.full_load(file)
    print('\033[1;32mConfig loaded')

@client.event
async def on_ready():
    invitelink = f'https://discordapp.com/api/oauth2/authorize?client_id={client.user.id}&permissions=544491302336&scope=applications.commands%20bot'
    print(f'Invite link for {client.user}:')
    print(invitelink)
    import database.__init__ as db
    db.create_tables(config)  # Create tables if they don't exist
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning)  # PandaSQL warning
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{config['app']['discord']['presence']['default-message']}"))
    loops.start()  # Start loop for updating the database


@tasks.loop(minutes=config['api']['refresh-interval'])
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


@slash.slash(name="notify", description="Get notifications from a station", options=[
    create_option(name='action', description='Choose what you want', required=True, option_type=3, choices=[create_choice(name="subscribe", value="subscribe"), create_choice(name="unsubscribe", value="unsubscribe", )]),
    create_option(name='station', description='Choose a station', required=True, option_type=3)
])
async def notify(ctx, *, action, station):
    from modules.commands.notify import index
    await index(ctx, action, station, config, client)


client.run(config['app']['discord']['token'])
