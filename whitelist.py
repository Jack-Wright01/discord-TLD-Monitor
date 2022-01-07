TLD = {
    # Each Top Level Domain (TLD) ranked 1-2 from least likely to be malicious (1) to more likely to contain malicious intent (2), while (3) is reserved for TLD statistically more likely to cause harm
    # Ranking based on Ionos' [Most popular domain extensions] (https://www.ionos.co.uk/digitalguide/domains/domain-extensions/most-popular-domain-extensions/)
    ".ac.uk": 1,
    ".au": 1,
    ".blog": 1,
    ".co": 1,
    ".com": 1,
    ".de": 1,
    ".edu": 1,
    ".fr": 1,
    "gg": 1,
    ".gov": 1,
    ".gov.uk": 1,
    ".io": 1,
    ".net": 1,
    ".org": 1,
    ".org.uk": 1,
    ".tech": 1,
    ".uk": 1,
    ".us": 1,

    #TIER 2
    ".in": 2,
    ".ir": 2,
    ".ua": 2,
    "xyz": 2,
}

def get(restrictionLevel):
    #Sort through TLDs, if in restriction range add to whitelist to send to app
    whitelist = []
    for key in TLD:
        if (TLD[key] <= restrictionLevel):
            whitelist.append(key)
    return whitelist