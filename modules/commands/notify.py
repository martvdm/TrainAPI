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


async def index(ctx, action, station, config, client):
    station = get_station(station)
    client_id = ctx.author.id
    from database.tables.notifications import create
    returnmessage = create(config, action, client_id, station)
    await ctx.send(returnmessage)


async def checknotifications(client, config):
    from database.tables.disruptions import check_action
    print(f'\033[93mChecking for notifications...')
    disruptions = get_disruptions()
    for disruption in disruptions:
        if "publicationSections" in disruption:
            action = check_action(disruption, config)
            if action != 'none':
                for station in disruption['publicationSections'][0]['section']['stations']:
                    users = find_users(config, station['stationCode'])
                    for user in users:
                        receiver = await client.fetch_user(user[0])
                        embed = discord.Embed(
                            title=f'{action}: {disruption["title"]} - {disruption["timespans"][0]["cause"]["label"]}',
                            description=f'{disruption["timespans"][0]["situation"]["label"]}', color=0xff5e5e)
                        if "additionalTravelTime" in disruption['timespans'][0]:
                            if "maximumDurationInMinutes" in disruption['timespans'][0]['additionalTravelTime']:
                                embed.add_field(name='Extra time:', value=f'{disruption["timespans"][0]["additionalTravelTime"]["maximumDurationInMinutes"]} minutes')
                            else:
                                embed.add_field(name='Extra time:', value=f'No extra travel time.', inline=True)
                        if "expectedDuration" in disruption:
                            embed.add_field(name='status', value=f'{disruption["expectedDuration"]["description"]}',
                                            inline=True)
                        if "lastUpdated" in disruption:
                            embed.author = discord.Embed.Author(name=f'Last updated: {station["lastUpdated"]}')
                        await receiver.send(embed=embed)
    print(f'\033[0m {len(disruptions)} disruptions found')
