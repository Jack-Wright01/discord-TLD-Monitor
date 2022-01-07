import discord
import whitelist
from random import randint

securityLevel = 1 # 1-3, 1 for most secure, 2+ for people feeling brave
whitelistedTLDs = []
unexpectedTLDs = []

def main():
    whitelistedVals = whitelist.get(securityLevel)
    for val in whitelistedVals: whitelistedTLDs.append(val)
    if (len(whitelistedTLDs) == 0): return log("[CRITICAL] failed to find whitelisted TLDs, abandoning bot startup", status="critical", consoleOnly=True)
    client = Client()
    #region CLIENT TOKEN
    client.run('')
    #endregion

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
        return print("Failed to obfuscate URL, dropping log")
    return obfuscatedUrl

def userAuthorised(author):
    """Check if specific roles can bypass the need for link checking
    Be cautious in using this as a compromised accoount with high roles will not be checked for suspicious links"""
    #TODO - Complete
    print("hello!")
    return False

def getTLD(url):
    """Gets Top Level Domain from String url"""
    for n in range(len(url)):
        TLD = url[-n:]
        if (TLD[0] == "."):
            #Remove anything additional at end of URL that isn't the TLD e.g. https://example.com/example
            try:
                TLD = TLD[:TLD.index("/")]
            except:
                pass
            return TLD.lower()
            
    print(f"Failed to find Top Level Domain in URL: {blankify(url)}")

def validTLD(TLD):
    """Checks whitelisted list of Top Level Domains to see if valid, and hopefully not malicious, link can stay"""
    """Logs if a new TLD is likely to be malicious or not, allowing for future updates"""
    if (TLD in whitelistedTLDs):
        return True
    if (TLD in unexpectedTLDs):
        log(f"Dumping url (see obfuscated in console) with TLD of {TLD}")
        return False
    log(f"Top Level Domain not detected in whitelist, dumping url (see console for obfuscatetd URL) with TLD of {TLD}, is this TLD safe?")
    unexpectedTLDs.append(TLD)
    return False

def log(msg, status="neutral", consoleOnly=False):
    """Logs update to console and (if provided) a discord channel, ideally for moderators to overlook without needing to view the console"""
    print(f"{status} - {msg}")

class Client(discord.Client):
    async def on_ready(self):
        print(f"{self.user} online")

    async def on_message(self, message):
        #if (userAuthorised): return
        print(f"Message from {message.author}: {message.content}")
        splice = message.content.split(" ")
        for url in splice:
           url = url.lower()
           if (isUrl(url) == True):
                TLD = getTLD(url)   
                if (TLD != None):
                    if (not validTLD(TLD)):
                        log(f"Obfuscated url: {blankify(url)}", consoleOnly=True)
                        await message.delete()
                    else:
                        log(f"Valid TLD {TLD} from {message.author}", consoleOnly=True)
                else:
                    log("Failed to find Top Level Domain in URL (see console for obfuscated URL)", status="warning")

if (__name__ == "__main__"):
    main()