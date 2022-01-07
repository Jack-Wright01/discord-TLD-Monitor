import discord
from discord import channel
import whitelist
import os
import asyncio
from random import randint
from dotenv import load_dotenv


load_dotenv()

STATUS_CHANNEL = 929060407367311441 #Channel ID of channel where the bot will push notifications
SECURITY_LEVEL = 1 # 1-3, 1 for most secure, 2+ for people feeling brave

unexpectedTLDs = []

def main():
    global whitelistedVals
    whitelistedVals = whitelist.get(SECURITY_LEVEL)
    if (whitelistedVals == None): return log("failed to find whitelisted TLDs, abandoning bot startup", status="critical", consoleOnly=True)
    global client
    client = Client()
    client.run(os.getenv("DISCORDKEY"))

async def log(msg, status="neutral", consoleOnly=False):
    """Logs update to console and (if provided) a discord channel, ideally for moderators to overlook without needing to view the console"""

    print(f"{status} - {msg}")
    if (consoleOnly == False):
        try:
            body = msg

            channel = client.get_channel(STATUS_CHANNEL)
            await channel.send(body)
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
    if (author == client.user):
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

async def validTLD(TLD):
    """Checks whitelisted list of Top Level Domains to see if valid, and hopefully not malicious, link can stay
    Logs if a new TLD is likely to be malicious or not, allowing for future updates"""
    if (TLD in whitelistedVals):
        return True
    if (TLD in unexpectedTLDs):
        log(f"Dumping url (see obfuscated in console) with TLD of {TLD}", consoleOnly=True)
    else:
        await log(f"Top Level Domain not detected in whitelist, dumping url (see console for obfuscatetd URL) with TLD of {TLD}, is this TLD safe?")
        unexpectedTLDs.append(TLD)    
    return False

class Client(discord.Client):
    async def on_ready(self):
        print(f"{self.user} online")
        try:
            channel = self.get_channel(STATUS_CHANNEL)
            await channel.send("Online")
        except:
            log("Discord channel to push notifications not set, will only update via console", consoleOnly=True)

    async def on_message(self, message):
        if (userAuthorised(message.author) == True): return
        splice = message.content.split(" ")
        for url in splice:
            url = url.lower()
            if (isUrl(url) == True):
                    TLD = getTLD(url)   
                    if (TLD != None):
                        if (not await validTLD(TLD)):
                            await log(f"Obfuscated url: {blankify(url)}", consoleOnly=True)
                            await message.delete()
                        else:
                            await log(f"Valid TLD {TLD} from {message.author}", consoleOnly=True)
                    else:
                        await log("Failed to find Top Level Domain in URL (see console for obfuscated URL)", status="warning")

if (__name__ == "__main__"):
    main()