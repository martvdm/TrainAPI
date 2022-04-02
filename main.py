import discord
import json
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option


client = commands.Bot(command_prefix='!')
slash = SlashCommand(client, sync_commands=True)

with open("config.json") as jsonfile:
    config = json.load(jsonfile)



@client.event
async def on_ready():
    print('\033[92mLoading data... \n \033[94mLoaded client: {0.user}'.format(client))
    print('\033[92mLoading commands...')
    print('\033[92mLoaded commands!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"ov-NL"))


@slash.slash(name="station", description="Get the current station")
async def station(ctx, *, station):
    import http.client, urllib.request, urllib.parse, urllib.error, base64
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': f"{config['Ocp-Apim-Subscription-Key']}",
    }
    params = urllib.parse.urlencode({
        # Request parameters
        'lang': f'{config["language"]}',
        'station': f'{station}',
        'uicCode': '',
        'dateTime': '',
        'maxJourneys': '6',
    })
    try:
        conn = http.client.HTTPSConnection('gateway.apiportal.ns.nl')
        conn.request("GET", "/reisinformatie-api/api/v2/departures?%s" % params, "{body}", headers)
        response = conn.getresponse()
        json_raw = response.read()
        json_data = json.loads(json_raw)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    embed = discord.Embed(title="Current station", description=f"{station}", color=0x00ff00)
    for departures in json_data['payload']['departures']:
        time = datetime.strptime(departures['plannedDateTime'], '%Y-%m-%dT%H:%M:%S+%f').strftime('%H:%M')
        embed.add_field(name=f"{departures['direction']}", value=f"**Type:** {departures['product']['shortCategoryName']} \n **Spoor:** {departures['plannedTrack']} \n **Vertrek:** {time}", inline=True)
    embed.set_footer(text="ov-NL")
    await ctx.send(embed=embed)








client.run(config['token'])