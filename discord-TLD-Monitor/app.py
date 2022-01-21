import discord as d
from discord.ext import commands, tasks
from dotenv import load_dotenv
from os import getenv
from random import randint
import whitelist, blacklist, config, log
import tldextract
import re
import datetime
import uuid

load_dotenv()
bot = commands.Bot(command_prefix=config.PREFIX, help_command=None)
startTime = datetime.datetime.now()

def findURLs(message):
    """Uses regex to find url(s) in message"""

    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, message)
    return [x[0] for x in url] # Returns list ['url0', 'url1', .. 'urln']

def getSuffix(url):
    """gets TLD from tldextract module"""

    try:
        suffix = tldextract.extract(url).suffix
        return suffix
    except:
        pass

def validChannel(channel):
    return channel.id == config.DEFAULT_CHANNEL.id

def userAuthorised(author):
    if (author == bot.user or author.bot): return True
    return False

@bot.event
async def on_ready():
    global blacklistUp, whitelistUp
    blacklistUp = blacklist.get()
    whitelistUp = whitelist.get()

    body0 = ""
    body1 = f"\n:globe_with_meridians: {whitelist.getSize()} Approved TLDs in this server\n\n:no_entry_sign: Blocked URLs: {blacklist.getSize()}\n\n:tools: Use `{config.PREFIX}help` for a list of commands. Alternatively, use `{config.PREFIX}help <cmd>` for info on a specific command"

    if (whitelistUp != False):
        body0 = ":white_check_mark: Whitelied TLD Library Active\n\n"
    else:
        body0 = ":x: Whitelied TLD Library **Inactive** - Strongly consider fixing ASAP\n\n"

    if (blacklistUp):
        body0 += ":white_check_mark: Blacklisted URL Library Active\n"
    else:
        body0 += ":x: Blacklisted URL Library **Inactive** - Strongly consider fixing ASAP\n"

    global channel
    channel = bot.get_channel(config.DEFAULT_CHANNEL)
    config.setDefaultChannel(channel)

    whitelistUpBool = True
    if (whitelistUp == False): whitelistUpBool = False

    log.terminal(f"{bot.user} Online\nStatus\n----------\nWhitelist TLD Library: {whitelistUpBool}\nBlacklist URL Library: {blacklistUp}\n")
    
    if (config.STARTUP_MSG == True):
        body = body0 + body1
        await log.discord(body=body, title="Top Level Domain Monitor", channel=channel, footer="")

    updateBlacklist.start()
    updateUptime.start()
    

@bot.event
async def on_message(message):
    """Detects blacklisted URLs, and URLs with unregistered TLDs"""

    urls = findURLs(message.content.lower())
    if (len(urls) > 0):
        for url in urls:
            #Check if blacklisted URL
            ticket = str(uuid.uuid1())[:8] # Get random num + letters from uuid for case references
            if (blacklist.isBlacklisted(url) == True):
                await message.delete()
                return await log.discord(body=f"Sent By: {message.author.mention}\nIn Channel: #{message.channel.mention}", title="Blacklisted URL Removed", color=d.Color.orange(), channel=channel, footer=f"Reference ticket {ticket}")
            
            #Check suffix and check with whitelist
            suffix = tldextract.extract(url).suffix
            if (suffix == None): return
            if (whitelist.isWhitelisted(suffix) == False):
                messageCreation = str(message.created_at)
                cleanTime = messageCreation[:messageCreation.index('.')] + " UTC"
                if (config.getMessageAction() == True):
                    await message.delete()
                    await log.discord(body=f"Deleted message with unwhitelisted TLD `.{suffix}` \n\n Author: {message.author.mention}\nChannel: {message.channel.mention}\nURL: `{url}`\nTimestamp: {cleanTime}", channel=channel, footer=f"Reference ticket {ticket}")
                    await log.discord(body=f"Hello {message.author.mention}! Your message includes a URL that is blocked in this server. If you think this is a mistake, please contact an admin", channel=message.channel, color= d.Color.orange(), footer=f"Reference ticket {ticket}")
                else:
                    await log.discord(body=f"Unwhitelisted TLD `.{suffix}` detected. Type `{config.PREFIX}add .{suffix}` to add to the whitelist \n\n Author: {message.author.mention}\nChannel: {message.channel.mention}\nURL: `{url}`\nTimestamp: {cleanTime}", channel=channel, footer=f"Reference ticket {ticket}")

    await bot.process_commands(message)

@bot.command()
async def add(ctx, arg=None):
    if (validChannel(ctx.message.channel) == False): return
    await whitelist.add(arg, ctx.author)


@bot.command()
async def remove(ctx, arg=None):
    if (validChannel(ctx.message.channel) == False): return
    await whitelist.remove(arg, ctx.author)


@bot.command(aliases=["whitelist"]) #Damn pesky double variable naming >:(
async def approved(ctx):
    if (validChannel(ctx.message.channel) == False): return
    list = whitelist.get()
    if (list == False): return await log.discord(body="Failed to get whitelist", channel=channel, color=d.Color.orange())
    body = ""
    for item in list:
        body += f"\n`{item}`"
    await log.discord(body=body, title="Approved TLDs", channel=channel)

@bot.command()
async def action(ctx, arg=None):
    if (validChannel(ctx.message.channel) == False): return
    if (arg==None): return await log.discord(body=f"No argument for `{config.PREFIX}action` given", footer=f"See `{config.PREFIX}help action` for help", channel=channel)
    arg = arg.lower()
    
    if (arg == "monitor"):
        await config.setMessageAction(False, ctx.message)
    elif (arg == "remove" or arg == "delete"):
        await config.setMessageAction(True, ctx.message)

@bot.command()
async def help(ctx, arg=None):
    """Handles help info in discord channel"""

    helpText= {
        "default": f"In efforts to counteract bots and compromised accounts linking malicious websites, this bot monitors messages and removes any message containing a URL with an unapproved TLD. \n\n The source code is still in development and available on [**Github**](https://github.com/Jack-Wright01/discord-TLD-Monitor)\n\n**Commands**\n\n`{config.PREFIX}whitelist` - Receive a list of approved TLDs on the server\n`{config.PREFIX}add` - Add an approved TLD to to the whitelist\n`{config.PREFIX}remove` - Remove a TLD from the whitetlist\n `{config.PREFIX}action` - Set the bots state when it detects an unapproved TLD\n\nFor information on each command's parameters, use `{config.PREFIX}help <CMD_NAME>`",
        "add": f"Add an approved TLD to to the whitelist \n\n **Example Usage**\n`{config.PREFIX}{arg} (.)org.uk`\n\nThe period at the start of the TLD is not required",
        "remove": f"Remove a TLD from the whitetlist \n\n **Example Usage**\n`{config.PREFIX}{arg} (.)org.uk`\n\nThe period at the start of the TLD is not required",
        "whitelist": f"View a list of approved Top Level Domains allowed in the server \n\n **Example Usage**\n`{config.PREFIX}{arg}`",
        "action": f"Set the bots state when it detects an unapproved TLD \n\n **Parameters** \n `monitor` - Detects and records TLDs to the console and/or status channel to be approved, does **not** delete any messages [DEFAULT]\n\n`remove` - Deletes any messages containing a URL with an aunapproved TLD\n\n **Example Usage**\n`{config.PREFIX}{arg} monitor`"

    }

    async def defaultHelp():
        await log.discord(body=helpText["default"], title="Top Level Domain Monitor", channel=config.getDefaultChannel())

    if (arg==None): return await defaultHelp()
    arg = arg.lower()
    try:
        await log.discord(body=helpText[arg], title=f"{config.PREFIX}{arg}", channel=config.getDefaultChannel())
    except:
        await defaultHelp()
    

@tasks.loop(seconds = config.BLACKLIST_REFRESH_INTERVAL)
async def updateBlacklist():
    """Updates blacklisted URL list, fetched from github page with updated json file (see blacklist.py)"""
    if (updateBlacklist.current_loop == 0): return # Skip first search, blacklist will have already been fetched with bot startup
    blacklistLen = blacklist.getSize()
    message = await log.discord(body=":hourglass: Updating blacklist...", channel=channel)

    if (blacklist.get()):
        delta = blacklist.getSize() - blacklistLen
        symbol = "+"
        if (delta < 0): symbol = "-"
        await log.edit(message, body=f"Blocked URL library updated ({symbol}{delta})", color=d.Color.green())
    else:
        await log.edit(message, body="Failed to find blocked URL library", color=d.Color.orange())

@tasks.loop(seconds = randint(20, 180))
async def updateUptime():
    dt = str(datetime.datetime.now() - startTime)
    dt = dt[:dt.index(".")]

    await bot.change_presence(activity=d.Game(name=f"for {dt} | {config.PREFIX}help"))


def main():
    bot.run(getenv("DISCORDKEY"))

if (__name__ == "__main__"):
    main()