import discord.ext
import mysql
import pandas
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from discord.ext import tasks
from discord import client
import asyncio
import json
from database.tables.notifications import find_users
from request import get_station, get_disruptions


async def index(ctx, station, config, client):
    station = get_station(station)
    stationcode = station['stationCode']
    client_id = ctx.author.id
    from database.tables.notifications import create
    returnmessage = create(config, client_id, stationcode)
    await ctx.send(returnmessage)

async def checknotifications(client, config):
    print(f'\033[93mChecking for notifications...')
    disruptions = get_disruptions()
    for disruption in disruptions:
        if "publicationSections" in disruption.keys():
            for station in disruption['publicationSections'][0]['section']['stations']:
                users = find_users(config, station['stationCode'])
                for user in users:
                    receiver = await client.fetch_user(user[0])
                    if receiver is not None:
                        embed = discord.Embed(title=f'{disruption["title"]} - {disruption["timespans"][0]["cause"]["label"]}', description=f'{disruption["timespans"][0]["situation"]["label"]}', color=0xff5e5e)
                        embed.add_field(name='Extra time:', value=f'{disruption["timespans"][0]["additionalTravelTime"]["maximumDurationInMinutes"]} minutes', inline=True)
                        await receiver.send(embed=embed)
    print(f'\033[0m {len(disruptions)} disruptions found')
