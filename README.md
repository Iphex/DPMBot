# DPMBot
A Discord Bot written in Python using Discord.py and mcstatus for Minecraft Server Queries
with Various Commands like:

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


You will need the libaries Discord.py and mcstatus
You can add both libaries with pip install discord and pip install mcstatus
Caution > mcstatus is abandoned. That means that there are a few bugs here and there


Personally, I followed the following bugfix for tcp and udp socket queries > https://github.com/Dinnerbone/mcstatus/pull/56
I have Messaged the Author on Twitter and hope that the bug will be fixed sometime soon :D


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
Referenz > https://github.com/tech189/danny-bot/blob/master/danny-bot.py
Used serveval other Minecraft bots / Discord bots for info and code, most importantly danny-bot
Tho much doesnt look like his code anymore, a lot is based upon his structure. Tho it had to be rewritten
for discord.py 1.0.1 since the libary was rewritten since he wrote that bot.


## General Information:
Well first of all, this is my first project and first time working with git / github
So I have no clue atm. how mergers etc. work, while I do have a general understanding of it :D
If you have any bugs or suggestions, go ahead.
Personally, I wouldnt use the bot just yet, until it restarts without problems and can be implemented into heroku
to run forever. Also the code is terrible. Did I say this is like my third python project? 


Other than that:
Discord.py works with Async. the call "await" ONLY works in functions which are called by "async def bla()"
I say this because, calling functions that should be awaited will raise an exception.

## Feature to come

Integrate the bot into Heroku using github repository and still hide the config.py file
and write something for the deployment there
Try to Communicate with AMP API for some additional info and maybe even server management.
Could make it so only the creator "author" is able to use those commands. 
Make the bot not throw an expection when somebody enters a command that does not exist

## Acknowledgments
https://github.com/tech189/danny-bot/blob/master/danny-bot.py for a lot the framework for the bot.
Allowed me to better understand how everything works.


Lerokko from https://www.reddit.com/r/discordapp/comments/8yn9hp/i_made_a_bot_that_shows_the_live_status_of_our/
for the framework around Rich Presence. 


Both of these Bots use the old discord.py and not the new one, meaning they both do not work with the newest version

## License
I have no clue if I need this but:
This project is licensed under the GNU General Public License - see [LICENSE.md] for details.


## Contributing
You can. Not sure how it works but you can!
