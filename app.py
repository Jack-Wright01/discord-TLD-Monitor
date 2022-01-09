import discord
from discord.ext.commands.errors import NotOwner
import whitelist
import os
from random import randint
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

STATUS_CHANNEL = 929060407367311441 #Channel ID of channel where the bot will push notifications


unexpectedTLDs = []


prefix = os.getenv("PREFIX")
bot = commands.Bot(command_prefix=prefix, help_command=None)

def main():
    global whitelistedVals
    whitelistedVals = whitelist.get()
    #if (whitelistedVals == None): return await log("failed to find whitelisted TLDs, abandoning bot startup", status="critical", consoleOnly=True)
    #client = Client()

def delMessage(state):
    global DEL_MESSAGES
    DEL_MESSAGES = state
    print("---", DEL_MESSAGES)

async def log(msg, status="neutral", consoleOnly=False, discordOnly=False, author="USER NOT FOUND", timestamp=None, footer="", title="", defaultChannel=None):
    """Logs update to console and (if provided) a discord channel, ideally for moderators to overlook without needing to view the console"""
    if (discordOnly == False):
        print(f"{status} - {msg}")
    
    if (consoleOnly == False):
        try:
            embed = None
            if (status == "critical"):
                embed=discord.Embed(title=title, description=msg, color=discord.Color.orange())
            elif (status == "success"):
                embed=discord.Embed(title=title, description=msg, color=discord.Color.green())
            else:
                embed=discord.Embed(title=title, description=msg, color=discord.Color.blue())
            if (footer != ""):
                embed.set_footer(text=footer)
            else:
                embed.set_footer(text=f"Posted by {author} on {timestamp} UTC")

            if (defaultChannel != None):
                await defaultChannel.send(embed = embed)
            else:
                channel = bot.get_channel(STATUS_CHANNEL)
                await channel.send(embed=embed)

        except: 
            await log("Error in sending notification to Discord", status="critical", consoleOnly=True)

def isUrl(str):
    """Checks http(s):// and . to identify if string is a potential url"""
    if ("http" in str and "." in str and "/" in str): return True

def blankify(url):
    """Obfuscates URL to break an automatic hyperlink to protect accidentally clicking in logs"""
    obfuscatedUrl = url
    for n in range(randint(8, 16)):
        location = randint(1, len(obfuscatedUrl)-1)
        if obfuscatedUrl[location] != " ":
            str0, str1 = obfuscatedUrl[:location], obfuscatedUrl[location:]
            obfuscatedUrl = str0 + " " + str1
    
    if (obfuscatedUrl == url):
        #Failed obfuscation - do not send further
        return ""
    return obfuscatedUrl

def userAuthorised(author):
    """Check if specific roles can bypass the need for link checking
    Be cautious in using this as a compromised accoount with high roles will not be checked for suspicious links"""
    if (author == bot.user):
        return True

    #Unauthorised
    return False

def getTLD(url):
    """Gets Top Level Domain from String url"""
    TLD = ""
    for n in range(len(url)):
        TLD = url[-n:]
        if (TLD[0] == "."):
            #Remove anything additional at end of URL that isn't the TLD e.g. https://example.com/example
            try:
                TLD = TLD[:TLD.index("/")]
            except:
                pass
            return TLD.lower()
    log(f"Failed to find Top Level Domain in URL: {blankify(url)}", consoleOnly=True)

async def validTLD(TLD, author, timestamp):
    """Checks whitelisted list of Top Level Domains to see if valid, and hopefully not malicious, link can stay
    Logs if a new TLD is likely to be malicious or not, allowing for future updates"""
    if (TLD in whitelistedVals):
        return True
    if (TLD in unexpectedTLDs):
        log(f"Dumping url (see obfuscated in console) with TLD of <{TLD}>", consoleOnly=True)
    else:
        await log(f"Top Level Domain not detected in whitelist, dumping url (see console for obfuscatetd URL) with TLD of `{TLD}`, is this TLD safe?", author=author, timestamp=timestamp)
        unexpectedTLDs.append(TLD)    
    return False


@bot.event
async def on_ready():
    print(f"{bot.user} Online")
    attempts = 0
    while (attempts < 3):
        try:
            channel = bot.get_channel(STATUS_CHANNEL)
            await log(f":white_check_mark:  Online \n\n:x: Auto delete non-whitelisted TLDs is **DISABLED** \n\n:globe_with_meridians: {len(whitelistedVals)} Approved TLDs in this server\n\n:page_facing_up: Use `{prefix}help` for a list of commands\n\n", status="neutral", title="Top Level Domain Monitor", footer="Developed by Jack!#2914", discordOnly=True)
            return
        except:
            attempts += 1
    if (attempts < 3):
        await log("Failed to connect to Discord channel, push notificattioons disabled",status="critical" ,consoleOnly=True)

@bot.event
async def on_message(message):
    if (userAuthorised(message.author) == True): return
    splice = message.content.split(" ")
    for url in splice:
        url = url.lower()
        if (isUrl(url) == True):
            TLD = getTLD(url)   
            if (TLD != None):
                if (not await validTLD(TLD, message.author, message.created_at)):
                    await log(f"Obfuscated url: {blankify(url)}", consoleOnly=True)
                    try:
                        if (DEL_MESSAGES == True):
                            await message.delete()
                    except: #DEL_MESSAGE Not defined, assume do NOT delete
                        pass
                else:
                    await log(f"Valid TLD <{TLD}> from {message.author}", consoleOnly=True)
            else:
                await log("Failed to find Top Level Domain in URL (see console for obfuscated URL)", status="warning", author=message.author, timestamp=message.created_at)
    await bot.process_commands(message)

@bot.command()
async def add(ctx, arg):
    newWhitelist, response, status = whitelist.add(arg)
    if (newWhitelist != None):
        whitelistedVals = newWhitelist
    await log(response, status=status, author=ctx.message.author, timestamp=ctx.message.created_at, discordOnly=True)

@bot.command()
async def remove(ctx, arg):
    newWhitelist, response, status = whitelist.remove(arg)
    if (newWhitelist != None):
        whitelistedVals = newWhitelist
    await log(response, status=status, author=ctx.message.author, timestamp=ctx.message.created_at, discordOnly=True)

@bot.command(aliases=["whitelist"]) #Damn pesky double variable naming >:(
async def approved(ctx):
    body = "Approved Top Level Domains in this server\n\n"
    for item in whitelistedVals:
        body = body + f"`{item}`\n"
    await log(body, status="neutral", author=ctx.message.author, timestamp=ctx.message.created_at, discordOnly=True)

@bot.command()
async def help(ctx, arg=None):
    try:
        arg = arg.lower()
        if (arg == "add"):
            await log(f"Add an approved TLD to to the whitelist \n\n **Example Usage**\n`{prefix}{arg} (.)org.uk`\n\nThe period at the start of the TLD is not required", title=f"{prefix}{arg}",author=ctx.message.author ,timestamp=ctx.message.created_at, discordOnly=True)
        elif (arg == "remove"):
            await log(f"Remove a TLD from the whitetlist \n\n **Example Usage**\n`{prefix}{arg} (.)org.uk`\n\nThe period at the start of the TLD is not required", title=f"{prefix}{arg}",author=ctx.message.author ,timestamp=ctx.message.created_at, discordOnly=True)
        elif (arg == "help"):
            await log(f"Get information about the bot and how to use the coommands \n\n **Example Usage**\n`{prefix}{arg}`", title=f"{prefix}{arg}",author=ctx.message.author ,timestamp=ctx.message.created_at, discordOnly=True)
        elif (arg == "whitelist"):
            await log(f"View a list of approved Top Level Domains allowed in the server \n\n **Example Usage**\n`{prefix}{arg}`", title=f"{prefix}{arg}",author=ctx.message.author ,timestamp=ctx.message.created_at, discordOnly=True)
        elif (arg == "action"):
            await log(f"Set the bots state when it detects an unaproved TLD \n\n **Parameters** \n `monitor` - Detects and records TLDs to the console and/or status channel to be approved, does **not** delete any messages [DEFAULT]\n\n`remove` - Deletes any messages containing a URL with an aunapproved TLD\n\n **Example Usage**\n`{prefix}{arg} monitor`", title=f"{prefix}{arg}",author=ctx.message.author ,timestamp=ctx.message.created_at, discordOnly=True)
        else:
            await log(f"In efforts to counteract bots and compromised accounts linking malicious websites, this bot monitors messages and removes any message containing a URL with an unapproved TLD. \n\n The source code is still in development and available on [**Github**](https://github.com/Jack-Wright01/discord-TLD-Monitor)\n\n**Commands**\n\n`{prefix}whitelist` - Recieve a list of approved TLDs on the server\n`{prefix}add` - Add an approved TLD to to the whitelist\n`{prefix}remove` - Remove a TLD from the whitetlist\n `{prefix}action` - Set the bots state when it detects an unaproved TLD\n\nFor information on each command's parameters, use `{prefix}help <CMD_NAME>", title="Top Level Domain Monitor", discordOnly=True)
    except:
        await log(f"In efforts to counteract bots and compromised accounts linking malicious websites, this bot monitors messages and removes any message containing a URL with an unapproved TLD. \n\n The source code is still in development and available on [**Github**](https://github.com/Jack-Wright01/discord-TLD-Monitor)\n\n**Commands**\n\n`{prefix}whitelist` - Recieve a list of approved TLDs on the server\n`{prefix}add` - Add an approved TLD to to the whitelist\n`{prefix}remove` - Remove a TLD from the whitetlist\n `{prefix}action` - Set the bots state when it detects an unaproved TLD\n\nFor information on each command's parameters, use `{prefix}help <CMD_NAME>", title="Top Level Domain Monitor", discordOnly=True)

@bot.command()
async def action(ctx, arg=None):
    if (arg == None): await log(f"No argument for `{prefix}action` given", footer=f"See `{prefix}help action` for more info", status="critical")
    arg = arg.lower()
    
    if (arg == "monitor"):
        delMessage(False)
        await log(f"Successfully set the bot to monitor URLs in this server, messages with unapproved Top Level Domains will **not** be deleted", footer=f"See `{prefix}help action` for more info", status="success", author=ctx.message.author, timestamp=ctx.message.created_at)
    elif (arg == "remove"):
        
        delMessage(True)
        await log(f"Successfully set the bot to remove URLs in this server, messages with unapproved Top Level Domains **will** be deleted", footer=f"See `{prefix}help action` for more info", status="success", author=ctx.message.author, timestamp=ctx.message.created_at)
    else:
        await log(f"`{arg}` is not a valid parameter", footer=f"See `{prefix}help action` for more info", status="critical")






@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Invalid argument(s)')

@remove.error
async def remove_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Invalid argument(s)')


if (__name__ == "__main__"):
    main()
    bot.run(os.getenv("DISCORDKEY"))

