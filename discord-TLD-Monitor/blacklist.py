import requests

def get():
    """Return list of blacklisted domains from github repo"""
    try:
        json = requests.get("https://raw.githubusercontent.com/nikolaischunk/discord-phishing-links/main/domain-list.json").json()
        global blacklist
        blacklist = json["domains"]
        return True
    except:
        return False

def isBlacklisted(val): return val.lower() in blacklist

def getSize(): return len(blacklist)