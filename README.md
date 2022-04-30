![Bot logo](https://cdn.discordapp.com/attachments/885185159522041867/962433451779309588/trainapi.PNG)

> A discord bot that can trace calamities &amp; departure/arrival times of stations. This bot uses the NS API, more information: https://apiportal.ns.nl/



# Setup:
**Create a discord APP/bot:**

> **Please read:** https://discordjs.guide/preparations/setting-up-a-bot-application.html

**Clone the repository:**
```bash
$ git clone https://github.com/martvdm/TrainAPI.git
```

**Install packages:**
```bash
pip install -r requirements.txt
```

**Create a config file:**
```bash
$ cp config.example.yaml config.yaml
```

**Fill in the config.yaml file:**
> **Please follow the instructions:**
>
> make an account at https://apiportal.ns.nl/signin?ReturnUrl=%2F (You need an account to gain acces to the api)
```yaml
app:
   name: trainAPI # Please fill in the name for your application
   language: en # Choose between (en & nl)
   version: 1.0.0 # PLEASE DONT CHANGE THIS
   maintenance-mode: false # (NOT IMPLEMENTED YET)
   storage:
      use-mysql: false # If false the application uses a local file system (JSON)
 # Customize your app with the following settings
   customization:
      theme-color: FFFFFF # This hexcolor-code will be used in embeds
#----------------------------------------------------------------------------
#  Discord bot settings
#----------------------------------------------------------------------------
   discord:
        token:  # Your discord bot token
        maintainers: # Discord id's of maintainers
            - 287598871373283329
        presence:
            show-last-station: false # If set to true: presence text will change when a user requests information about station.
            ## ^^^ Please note that this will affect the performance
            default-message: "TrainAPI"
            default-type: PLAYING #PLAYING, LISTENING, WATCHING, STREAMING

#------------------------------------------------------------------------------
# Database
# ONLY SUPPORTS MYSQL
#------------------------------------------------------------------------------
# Please note that "use-mysql" must be set to true in the "app" section above, else this section will be ignored.
#------------------------------------------------------------------------------
database:
  host: localhost
  port: 3306
  user: root
  password: root
  database: trainapi

#------------------------------------------------------------------------------
# All api credentials
#------------------------------------------------------------------------------
api:
  refresh-interval: 3 # In minutes
  # ^^^ 3 minutes IS RECOMMENDED, TO MUCH MAY AFFECT THE PERFORMANCE ALSO YOU CAN BE RATE LIMITED BY NS
  ns-primary-key: SECRETKEY #PRIMARY KEY 
  # ^^^ This key can be found in the APIPORTAL account dashboard
```

**Run the bot:**
```bash
$ python main.py
```

**Invite the bot to your server:**

> When the application starts up it will send a log in the console. 
> This log will contain the generated invite link.

Example:
```bash
$ Config loaded
$ Invite link for TrainAPI#5430:
$ https://discordapp.com/api/oauth2/authorize?client_id=959101335008063558&permissions=544491302336&scope=applications.commands%20bot
                ^^^ This link redirects to the invite page.
```

