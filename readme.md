# Discord Top Level Domain (TLD) Monitor

In efforts to counteract bots and compromised accounts linking malicious websites, this python bot attempts to catch malicious messages, ideal for large servers. It does this in three ways:

1. Detect if a message contains a URL, if so, compare the TLD to a whitelist of approved TLDs, remove message if it contains unapproved TLD 
2. Detect if a message contains a URL, if so, check if the URL(s) are not included in [an actively maintained list of known malicious links](https://github.com/nikolaischunk/discord-phishing-links)
3. Detect if a message contains a URL, **AND** includes "nitro"

 
## Dependencies & Setup

Ensure an environment variable, ```DISCORD_KEY``` exists on the host machine with your Bot's client token available [here](https://discord.com/developers/applications).

Ensure the following Python packages are installed on the host machine:

```bash
pip install tldextract
pip install dotenv
pip install discord
pip install uuid
```

Navigate to ```config.py``` and set your ```DEFAULT_CHANNEL``` to the channel ID that the logged messages will display to, and  ensure the bot has permissions to view,  **and** post in the channels that it should be monitoring

## Example
Below shows the output of the bot deleting malicious messages as intended as soon as they are posted. In this instance it is because the whitelist for this server does not include the TLD ```.gift```

![Screenshot of bot working](https://i.imgur.com/7QPaSCU.png)

## Adding/Removing from the whitelist

Along with the bot's prefix (default $), ```add``` and ```remove``` can be used for users to add/remove to the server's whitelist in real time without having to alter any files. For more commands, use ```help``` along with your assigned prefix.

## Recommendations
1. The bot has two modes when conditions 1, and 3 (but not 2) is met, *monitor* mode and *remove* mode. Monitor mode does not delete the message, but only logs the message to the provided. It is **strongly** recommended you trial the bot using the monitor only mode so that you are able to gather a large set of TLDs which will need adding to the server's whitelist. This is recommended to allow for your moderator team to slowly build up a suitable whitelist whilst having minimal impact on your users. 

2. Anyone who has access to the ```DEFAULT_CHANNEL``` can run commands through the bot, and so it is recommended that the logging channel is only visible to a team that you want to monitor the server and alter the whitelist.

## License
[MIT](https://choosealicense.com/licenses/mit/)