import json, log, config
import discord as d

#Default approved TLDs
TLD = [".ac.uk",".au",".blog",".co",".com",".de",".edu",".fr",".gg",".gov",".gov.uk",".io",".net",".org",".org.uk",".tech",".uk",".us"]

def cleanSuffix(s):
    """Converts TLD to include period for consistent logging
    e.g "co.uk" -> ".co.uk"""

    s = s.lower()
    if (s[:1] != "."): s = "." + s
    return s

def get():
    """Attempts to create/load TLD list
    Returns bool/list if TLD list exists"""

    try:
        with open("whitelist.json") as f:
            global whitelist
            whitelist = json.load(f)
            return whitelist
    except:
        whitelist = create()

def create():
    """Call to make new whitelist.json"""
    with open("whitelist.json", "w") as jsonFile:
        json.dump(TLD, jsonFile)
    return TLD

def save():
    """Update and save json file"""

    with open("whitelist.json", "w") as jsonFile:
        json.dump(whitelist, jsonFile)
    return whitelist

async def add(val=None, author=None):
    """Add value to whitelist"""
    message = await log.processing(channel=config.getDefaultChannel())
    if (val == None): return await log.edit(messageObj=message, body="No argument given", footer=f"Use `{config.PREFIX}help add` for help", color=d.Color.orange())
    if (author == None): return await log.edit(body="Cannot parse command without an author being logged, contact bot developer", color=d.Color.light_gray())
    
    val = cleanSuffix(val)
    if (isWhitelisted(val) == False):
        whitelist.append(val)
        whitelist.sort()
        save()
        get()
        await log.edit(messageObj=message, body=f"`{val}` added successfully", footer="", color=d.Color.green())
        log.terminal(f"`{val}` added successfully by {author} ({author.id}) on [{message.created_at}]")
    else:
        await log.edit(messageObj=message, body=f"`{val}` already whitelisted", color=d.Color.orange())
        

async def remove(val=None, author=None):
    """Remove value from whitelist"""
    message = await log.processing(channel=config.getDefaultChannel())
    if (val == None): return await log.edit(messageObj=message, body="No argument given", footer=f"Use `{config.PREFIX}help remove` for help", color=d.Color.orange())
    if (author == None): return await log.edit(messageObj=message, body="Cannot parse command without an author being logged, contact bot developer", color=d.Color.light_gray())

    val = cleanSuffix(val)
    if (isWhitelisted(val) == True):
        whitelist.remove(val)
        save()  
        get()
        await log.edit(messageObj=message, body=f"`{val}` removed successfully", footer="", color=d.Color.green())
        log.terminal(f"`{val}` removed successfully by {author} ({author.id}) on [{message.created_at}]")
    else:
        await log.edit(messageObj=message, body=f"`{val}` could not be found in whitelist", color=d.Color.orange())

def isWhitelisted(val):
    val=cleanSuffix(val)
    return val in whitelist

def getSize(): return len(whitelist)
    