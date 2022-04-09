![Bot logo](https://cdn.discordapp.com/attachments/885185159522041867/962433451779309588/trainapi.PNG)

A discord bot that can trace calamities &amp; departure/arrival times of stations. This bot uses the NS API, more information: https://apiportal.ns.nl/

# Made with Discord.py

# Setup:
**Create a discord APP/bot:**

**Please read:** https://discordjs.guide/preparations/setting-up-a-bot-application.html

**Clone the repository:**
```bash
git clone https://github.com/martvdm/TrainAPI.git
```

**Install packages:**
```bash
pip install -r requirements.txt
```

**Create a config file:**
```bash
cp config.example.json config.json
```

**Fill in the config.json file:**

```json
{
  "token": "BOT_TOKEN",  <-- Replace with your discord-bot token
  "language": "en, nl", <-- Your language
  "api": {
    ---> The NS-Primary key is needed to gain acces to the API
    ---> make an account at "https://apiportal.ns.nl/signin?ReturnUrl=%2F"
    "NS-PRIMARY": "Ocp-Apim-Subscription-Key" <-- Replace with your NS-Primary key
  },
  "app": {
    "author": "Mart",
    "invite": "https://discord.com/api/oauth2/authorize?client_id=CLIENT_ID&permissions=8&scope=bot%20applications.commands", <-- Modify the url with your client id
    "testing": {
      "server": "TEST-SERVER-ID", <-- Replace with your test server id (optional)
      "channel": "TEST-CHANNEL-ID" <-- Replace with your test channel id (optional)
    }
  },
  "database": { 
    "host": "localhost", <-- Replace with your database IP
    "port": 3036, <-- Replace with your database port
    "database": "database", <-- Replace with your database name
    "username": "root", <-- Replace with your database username
    "password": ""  <-- Replace with your database password
  }
}
```

**Run the bot:**
```bash
python3 main.py
```

**Invite the bot to your server**

replace the CLIENT_ID with the client id of your bot

```bash
https://discordapp.com/api/oauth2/authorize?client_id=CLIENT_ID&permissions=8&scope=bot%20applications.commands
```

