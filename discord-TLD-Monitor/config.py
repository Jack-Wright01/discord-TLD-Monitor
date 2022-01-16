import log, config
import discord as d

#For Bot Token, make new environment variable
PREFIX = "$"
DEFAULT_FOOTER = f"{PREFIX}help for more info"
DEFAULT_CHANNEL = 931245164620566608
STARTUP_MSG = True
DELETE_MESSAGES = False
BLACKLIST_REFRESH_INTERVAL = 60 * 60 * 4

#Getters 'n Setters
def getMessageAction(): return DELETE_MESSAGES
def getDefaultChannel(): return DEFAULT_CHANNEL

async def setMessageAction(bool, message=None):
    if (message == None): return await log.discord(body="Cannot parse command without an author being logged, contact bot developer", channel=config.getDefaultChannel(), color=d.Color.light_gray())
    global DELETE_MESSAGES
    DELETE_MESSAGES = bool
    if (bool == True):
        pass
        #TODO-Add log saying they wont be deleted oops how did i forget this
    else:
        await log.discord(body=f"Successfully set the bot to monitor URLs in this server, messages with unapproved Top Level Domains will **not** be deleted", footer=f"See `{PREFIX}help action` for more info", channel=DEFAULT_CHANNEL, color=d.Color.green())
    
    log.terminal(f"Successfully set the bot to monitor URLs in this server - by {message.author} ({message.author.id}) on {message.created_at}")

def setDefaultChannel(chan): 
    global DEFAULT_CHANNEL
    DEFAULT_CHANNEL = chan