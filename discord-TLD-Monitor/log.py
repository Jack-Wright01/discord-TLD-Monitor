import config
import discord as d
from discord.ext import commands

async def discord(body=None, title="", footer=config.DEFAULT_FOOTER, channel=config.DEFAULT_CHANNEL, color=d.Color.blue()):
    """Push to discord channel with embeded design"""
    embed = d.Embed(title=title, description=body, color=color)
    embed.set_footer(text=footer)

    return await channel.send(embed=embed)

async def edit(messageObj=None, body=None, title="", footer=config.DEFAULT_FOOTER, color=d.Color.blue()):
    """Edit discord text with embed"""
    if (messageObj == None): return terminal("Failed to update message, no message object assigned")
    embed = d.Embed(title=title, description=body, color=color)
    embed.set_footer(text=footer)
    return await messageObj.edit(embed=embed)

async def processing(channel):
    """Creates and returns embed message of default processing text"""
    return await discord(body=":hourglass: Processing", title=" ", channel=config.getDefaultChannel())

def terminal(body):
    print(body)
