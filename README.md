# DPMBot
A Discord Bot written in Python using Discord.py and mcstatus for Minecraft Server Queries
with Various Commands like(so many):

#mc or #status > Checks the server status, Gotta add a picture here

#list > lists the current online players

#info > Gives a little info about the bot

#help > Gives all commnands

It also works with Rich Presence, showing the current server Status, Players Playing and Ping

## Getting Started
You have to create a discord bot, and add it to your server.
https://www.digitaltrends.com/gaming/how-to-make-a-discord-bot/ Follow Step 2 - 4 for Instructions.

### Prerequisites
I used Python 3.7.3, but every Python 3.x Version should work (probably)


You will need the libaries Discord.py (1.0.1 and up) and mcstatus. See [requirements.txt]
You can add both libaries with pip install discord and pip install mcstatus


Caution > mcstatus is abandoned. !!! Not anymore since 07.05.2019. Expect Updates here.


We need mcstatus for queries and faster pings. That way we do not have to use a API and wait for those

### Installing
config.py has certain attributes that have to be set. It contains various possibly harmful imformation like your Discord Bot Token, which is why it is not included in this Repository. The Repository does have a example File [ex_config.py]


Once config.py is set and configured with data like your server, your Bots token and/or Favicons



Once that is done, you can now open notify_server.py in whatever Environment you like, and start it.
The bot should (hopefully) join your Server and accept Commands with your prefix (mine is #)
Use #help for imformation.
I have not tested this on any Other PC yet.

## Deployment
See Features to come


## General Information:
Well first of all, this is my first real project and first time working with git / github.
So I have no clue atm. how mergers etc. work, while I do have a general understanding of it :D
If you have any bugs or suggestions, go ahead.
Personally, I wouldnt use the bot just yet, until it can be implemented into heroku
to run forever. Also the code is terrible.


## Features to come

Integrate the bot into Heroku using github repository and still hide the config.py file
and write something for the deployment there


Try to Communicate with AMP API for some additional info and maybe even server management.



## License
This project is licensed under MIT, see [LICENSE.md] for details.
