import discord
import json
import http.client, urllib.request, urllib.parse, urllib.error, base64
from datetime import datetime, timedelta
from discord.ext import commands
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_components import ComponentContext, create_actionrow, create_button, create_select, create_select_option
from discord_slash.model import ButtonStyle
import __api__
from request import get_station


async def index(ctx, station, config, client):
    station = get_station(station)
    stationcode = station['stationCode']
    embed = discord.Embed(title="Station: ", description=f"{station['name']}", color=0x000065)
    from __api__ import nsapi
    params = urllib.parse.urlencode({
        # Request parameters
        'lang': f'{config["language"]}',
        'station': f'{stationcode}',
        'uicCode': '',
        'dateTime': '',
        'maxJourneys': '99',
    })
    url = f'/reisinformatie-api/api/v2/departures'
    json_data = nsapi(url, params)
    departcount = 0
    for departures in json_data['payload']['departures']:
        time = datetime.strptime(departures['plannedDateTime'], '%Y-%m-%dT%H:%M:%S+%f').strftime('%H:%M')
        hournow = (datetime.now() + timedelta(hours=1)).strftime('%H:%M')
        if time <= hournow:
            departcount += 1
    embed.add_field(name="Trains per hour:", value=f"{departcount}", inline=True)
    embed.set_image(url=f"https://www.ns.nl/static/rio/apps/stationsinformatie/7.1.41/assets/heroes/{stationcode.lower()}.jpg")
    buttons = [
        create_button(
            style=ButtonStyle.blue,
            label="Faciliteiten"
        ),
        create_button(
            style=ButtonStyle.blue,
            label="Vertrektijden",

        ),
        create_button(
            style=ButtonStyle.red,
            label="Calamiteiten",
        ),
    ]
    action_row = create_actionrow(*buttons)
    await ctx.send(embed=embed, components=[action_row])


async def departures(ctx, station, config, client):
    station = get_station(station)
    from request import get_train
    stationcode = station['stationCode']
    from __api__ import nsapi
    params = urllib.parse.urlencode({
        # Request parameters
        'lang': f'{config["language"]}',
        'station': f'{stationcode}',
        'uicCode': '',
        'dateTime': '',
        'maxJourneys': '6',
    })
    url = f'/reisinformatie-api/api/v2/departures'
    json_data = nsapi(url, params)
    cancelledembed = discord.Embed(title="Cancelled:", color=0xff5e5e)
    embed = discord.Embed(title="Departures station: ", description=f"{station['name']}", color=0x000065)
    for departures in json_data['payload']['departures']:
        ridenumber = departures['product']['number']
        train = get_train(ridenumber)
        time = datetime.strptime(departures['plannedDateTime'], '%Y-%m-%dT%H:%M:%S+%f').strftime('%H:%M')
        if departures['cancelled'] == False:
            embed.add_field(name=f"{departures['direction']}",
                            value=f"**Type:** {departures['product']['shortCategoryName']} \n **Treintype:** {train['type']}{train['lengte']} \n **Spoor:** {departures['plannedTrack']} \n **Vertrek:** {time}",
                            inline=True)
        else:
            cancelledembed.add_field(name=f"{departures['direction']}",
                                     value=f"{departures['product']['shortCategoryName']} | {departures['messages'][0]['message']} \n van {time}",
                                     inline=False)
    embed.set_footer(text="ov-NL")
    if cancelledembed.fields:
        await ctx.send(embed=cancelledembed)
    print('\x1b[6;30;42m' + f'{ctx.author} requested station: {station["name"]}' + '\x1b[0m')
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"Station {station['name']}"))
    await ctx.send(embed=embed)
    return

# create_select(
#     options = [
#         create_select_option("test", value="test"),
#         create_select_option("test2", value="test2"),
#         create_select_option("test3", value="test3"),
#     ],
#     placeholder="Selecteer een optie",
#     min_values=1,
#     max_values=2,
# )