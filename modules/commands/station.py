import discord
import json
import http.client, urllib.request, urllib.parse, urllib.error, base64
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext
import __api__

async def index(ctx, station, config, client):
    from __api__ import get_station
    station = get_station(station)
    from __api__ import get_train
    stationcode = station['stationCode']
    from __api__ import request_nsapi
    params = urllib.parse.urlencode({
        # Request parameters
        'lang': f'{config["language"]}',
        'station': f'{stationcode}',
        'uicCode': '',
        'dateTime': '',
        'maxJourneys': '6',
    })
    url = f'/reisinformatie-api/api/v2/departures'
    json_data = request_nsapi(url, params)
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
        await  ctx.send(embed=cancelledembed)
    print('\x1b[6;30;42m' + f'{ctx.author} requested station: {station["name"]}' + '\x1b[0m')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Station {station['name']}"))
    await ctx.send(embed=embed)
    return
