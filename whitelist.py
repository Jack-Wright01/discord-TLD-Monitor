import json

whitelist = None

TLD = [
    # Default trusted TLDs
    ".ac.uk",
    ".au",
    ".blog",
    ".co",
    ".com",
    ".de",
    ".edu",
    ".fr",
    ".gg",
    ".gov",
    ".gov.uk",
    ".io",
    ".net",
    ".org",
    ".org.uk",
    ".tech",
    ".uk",
    ".us",
]

def clean(val):
    """Converts TLD into standard format with period at the front and all lowercase"""
    val = val.lower()
    if (val[:1] != "."):
        val = "." + val
    return val

def get():
    """Sort through TLDs, if in restriction range add to whitelist to send to app"""
    try:
        with open("whitelist.json") as f:
            whitelist = json.load(f)
            TLD = whitelist
    except:
        whitelist = create()
    
    return whitelist

def create():
    """Create whitelist JSON file with saved approved words"""
    save()

def save():
    """Update whitelist to JSON file"""
    with open('whitelist.json', 'w') as jsonFile:
        json.dump(TLD, jsonFile)
    return TLD

def add(val):
    """Add TLD to JSON"""
    val = clean(val)

    if (val in TLD):
        return None, f"`{val}` is already in the whitelist", "critical"

    try:
        TLD.append(val)
        whitelist = save()
        return whitelist, f"`{val}` added successfully", "success"
    except:
        return None, f"failed to add `{val}`", "critical"

def remove(val):
    """Remove TLD to JSON"""
    val = clean(val)

    try:
        if (val in TLD):
            TLD.remove(val)
            whitelist = save()
            return whitelist, f"`{val}` removed successfully", "success"
        else:
            return None, f"`{val}` does not exist", "critical"
    except:
        return None, f"failed to remove `{val}`", "critical"