import requests

blacklist = None

def get():
    """Return list of blacklisted domains from github repo"""
    try:
        json = requests.get("https://raw.githubusercontent.com/nikolaischunk/discord-phishing-links/main/domain-list.json").json()
        global blacklist
        blacklist = json["domains"]
        return True, f":white_check_mark: Blacklisted URL library active", "success"
    except:
        return False, f"Failed to get blacklisted URL library", "critical"

def isBlacklisted(val):
    """Returns if val is blacklisted or not"""
    try:
        val = str(val)
        if (val in blacklist):
            return True
    except:
        return False

def getSize():
    return len(blacklist)