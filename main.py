import discord
import json
from datetime import datetime
import modules as module
from discord.ext import commands
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option


client = Bot(command_prefix='!')
slash = SlashCommand(client, sync_commands=True)

with open("config.json") as jsonfile:
    config = json.load(jsonfile)

@client.event
async def on_ready():
    print('\033[92mLoading data... \n \033[94mLoaded client: {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"ov-NL"))

@slash.slash(name="station", description="Get the current station")
async def station(ctx, *, station):
    import http.client, urllib.request, urllib.parse, urllib.error, base64
    headers = {
        'Ocp-Apim-Subscription-Key': f"{config['api']['NS-PRIMARY']}",
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
        await ctx.send('Het ophalen van de API is mislukt. Probeer het later opnieuw.')
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    cancelledembed = discord.Embed(title="Cancelled:", color=0xff5e5e)
    embed = discord.Embed(title="Current station", description=f"{station}", color=0x000065)
    for departures in json_data['payload']['departures']:
        time = datetime.strptime(departures['plannedDateTime'], '%Y-%m-%dT%H:%M:%S+%f').strftime('%H:%M')
        if departures['cancelled'] == False:
            embed.add_field(name=f"{departures['direction']}", value=f"**Type:** {departures['product']['shortCategoryName']} \n **Spoor:** {departures['plannedTrack']} \n **Vertrek:** {time}", inline=True)
        else:
            cancelledembed.add_field(name=f"{departures['direction']}", value=f"{departures['product']['shortCategoryName']} | {departures['messages'][0]['message']} \n van {time}", inline=False)
    embed.set_footer(text="ov-NL")
    if cancelledembed.fields:
        await ctx.send(embed=cancelledembed)
    await ctx.send(embed=embed)

client.run(config['token']);