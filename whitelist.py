TLD = {
    # Each Top Level Domain (TLD) ranked 1-2 from least likely to be malicious (1) to more likely to contain malicious intent (2), while (3) is reserved for TLD statistically more likely to cause harm
    # Ranking based on Ionos' [Most popular domain extensions] (https://www.ionos.co.uk/digitalguide/domains/domain-extensions/most-popular-domain-extensions/)
    ".com": 1,
    ".org": 1,
    ".net": 1,
    ".ir": 3,
    ".in": 2,
    ".uk": 1,
    ".ac.uk": 1,
    ".org.uk": 1,
    ".au": 1,
    ".de": 1,
    ".ua": 2,
    ".tech": 1,
    ".edu": 1,
    # More likely malicious TLDs taken from https://www.bleepingcomputer.com/news/security/these-are-the-top-level-domains-threat-actors-like-the-most/
    ".zw": 3,
    ".ru": 3,
    ".bd": 3,
    ".ke": 3,
    ".am": 3,
    ".sbs": 3,
    ".date": 3,
    ".pw": 3,
    ".quest": 3,
    "cd": 3,
    "bid": 3,
    "support": 3, #TODO - Check TLD is .support rather than support.(microsoft... e.g) or will throw false +ve
    "help": 3, #TODO - See above
    "email": 3,
    "info": 3,
    "xyz": 2,
    "gg": 2,
}

def get(restrictionLevel):
    #Sort through TLDs, if in restriction range add to whitelist to send to app
    whitelist = []
    for key in TLD:
        if (TLD[key] <= restrictionLevel):
            whitelist.append(key)
    return whitelist