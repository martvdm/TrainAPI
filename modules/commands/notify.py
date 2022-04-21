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
from database.tables.notifications import create
from request import get_station

async def index(ctx, station, config, client):
    station = get_station(station)
    stationcode = station['stationCode']
    client_id = ctx.author.id
    from database.tables.notifications import create
    create(config, client_id, stationcode)
    embed = discord.Embed(title="Notify", description="No response from DB service. (Please contact maintainer)", color=0xff5e5e)
    embed.add_field(name="Tried to create a notification for:", value=f"Station:{station['name']} \n Client: {client_id}", inline=False)
    await ctx.send(embed=embed)
