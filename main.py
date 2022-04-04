import discord
import json
import http.client, urllib.request, urllib.parse, urllib.error, base64
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext

client = Bot(command_prefix='!')
slash = SlashCommand(client, sync_commands=True)

with open("config.json") as jsonfile:
    config = json.load(jsonfile)

@client.event
async def on_ready():
    print('\033[92mLoading data... \n \033[94mLoaded client: {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"ov-NL"))

@slash.slash(name="station", description="Get the current")
async def station(ctx, *, station):
    from __api__ import get_station
    station = get_station(station)
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
    type = 'departures'
    api = 'reisinformatie-api/api'
    json_data = request_nsapi(type, params, api)
    cancelledembed = discord.Embed(title="Cancelled:", color=0xff5e5e)
    embed = discord.Embed(title="Current station", description=f"{station['description']}", color=0x000065)
    print(json_data)
    for departures in json_data['payload']['departures']:
        time = datetime.strptime(departures['plannedDateTime'], '%Y-%m-%dT%H:%M:%S+%f').strftime('%H:%M')
        if departures['cancelled'] == False:
            embed.add_field(name=f"{departures['direction']}", value=f"**Type:** {departures['product']['shortCategoryName']} \n **Spoor:** {departures['plannedTrack']} \n **Vertrek:** {time}", inline=True)
        else:
            cancelledembed.add_field(name=f"{departures['direction']}", value=f"{departures['product']['shortCategoryName']} | {departures['messages'][0]['message']} \n van {time}", inline=False)
    embed.set_footer(text="ov-NL")
    if cancelledembed.fields:
        await ctx.send(embed=cancelledembed)
    print('\x1b[6;30;42m' + f'{ctx.author} requested station: {station["description"]}' + '\x1b[0m')
    await ctx.send(embed=embed)

client.run(config['token']);