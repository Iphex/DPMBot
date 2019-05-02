# Written for Python 3.7.x

import asyncio
import datetime
import json
import logging
import os
import urllib.request

import discord
import mcstatus
from discord.ext import commands

import config
#pylint might be annoying here, since he for some reason cant see config
#unsure how to exactly prevent this :
TOKEN = config.discord_token
client = commands.Bot(command_prefix='#')

logger = logging.getLogger()
handler = logging.FileHandler("dpm_bot.log", mode="a")
formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
# I have actually no clue how this works, but I need to implement logging :D


pingFrequency = 60
# in Seconds


def mc_info(address, port):
    """
        Mc Info uses mcstatus to ping a Minecraft Server and query Information about it
        without having to use an Middleman API, increasing performance and allowing for 
        a bit more customization.
        The Implementation should work with a Port 25565, but I have only tested it with
        my own servers Port. Custom Ports Work.
    """
    if port is None:
        print("No Port specified using standard 25565")
        server = mcstatus.MinecraftServer.lookup(address)
    else:
        server = mcstatus.MinecraftServer(address, port)

    mc_log = config.minecraft_server_log
    if config.server_name_no_caps in address:
        response = urllib.request.urlopen("https://api.ipify.org/?format=json")
        data = response.read().decode("utf-8")
        jsondata = json.loads(data)
        ip = jsondata["ip"]
    else:
        try:
            ip = address
        except:
            ip = None
    try:
        # usually you would use server.Status here, but for some reason it stopped working :D
        # If the recipent Server is sleeping, the ping will Fail! Some Servers do have a feature
        # to wake up when pinged
        info = server.ping()
        status = True
        try:
            #See server.query file for info on what information query gives
            query = server.query()
            players_names = query.players.names #ex ['user1','user2','user2']
            players_online = query.players.online
            players_max = query.players.max
            try:
                software = query.software.brand #ex. Vanilla
                version = query.software.version #ex. 1.14
                description = query.motd
                maps = query.map
                latency = str(info)
            except:
                software = None
                version = None
                description = None
                latency = None
                maps = None
                address = None
                players_max = None
        except:
            players_online = query.players.online
            players_names = None
    except:  
        #to make sure nothing is called that hasn't been set before
        print("status Failed!")
        status = False
        players_online = None
        players_names = None
        software = None
        version = None
        description = None
        latency = None
        maps = None
        address = None
        players_max = None
        last_online = ["", "", "", ""]
    if software == "vanilla":
        try:
            # this doesnt work. Copied this over and have to go through and understand this all again.
            old_log = None
            time_started = None
            last_player = None
            last_time = None
            get_path_time = os.path.getmtime(mc_log)
            nicetime = datetime.datetime.fromtimestamp(get_path_time)
            if nicetime.date() < datetime.datetime.today().date():
                old_log = True
            else:
                old_log = False
            if old_log is False:
                with open(mc_log, mode="r", encoding="utf-8") as file:
                    for line in file:
                        if line[11:58] == "[Server thread/INFO]: Starting Minecraft server":
                            time_started = line[1:9]
                with open(mc_log, mode="r", encoding="utf-8") as file:
                    for line in file:
                        if line[11:33] == "[Server thread/INFO]: " and line[-15:] == " left the game\n":
                            last_player = line[33:-15]
                            last_time = line[1:9]
            last_online = [old_log, time_started, last_player, last_time]
        except:
            last_online = ["", "", "", ""]
    #Logging threw an error here, so I gotta check it up again.       
    #logger.info(status, ip, players_online, players_names, software, version, description, last_online, latency, maps, address, players_max)
    return status, ip, players_online, players_names, software, version, description, last_online, latency, maps, address, players_max

def load_functions():
    """
        Here are serveval Decorators using Discord.py to react to Commands in Chat.
        for Example > #hello in chat would trigger @client.command and do whatever _hello is.

    """
    client.remove_command('help')

    @client.command(aliases=['hello', 'Hello', 'Hi', 'hi'])
    async def _hello(message):
        """
            Command to say something and mention the author who asked.
        """
        msg = 'Hello {0.author.mention}! 👋'.format(message)
        await message.send(msg)

    @client.command(aliases=['stop', 'Stop'])
    async def _stop(message):
        """
            Raising a keyboardInterrupt and not SystemExit, because we catch both but turn SystemExit
            into a Restart of the Bot, while KeyboardInterrupt stops it. 
            This is Abuseable, should probl remove once you are done testing, or something.
        """
        msg = 'Byyyyyiiiee {0.author.mention}, 👋'.format(message)
        await message.send(msg)
        raise KeyboardInterrupt

    @client.command(aliases=['shhhh'])
    async def _shutup(message):
        """
            A command for a certain human being who thinks this bot
            is being abused...
        """
        msg = 'Thank you my godemporer {0.author.mention}, I hereby order {} to shut the fuck up, I am here of Free Will! 👋'.format(message, config.a_certain_user)
        await message.send(msg)

    @client.command(aliases=['info', 'information'])
    async def _info(message):
        """
            Info Command giving out the Code Source
        """
        #TODO Figure out how to make it a direct link, not sure if this works atm
        msg = 'For More information regarding this bot, visit https://github.com/Iphex/DPMBot'
        await message.send(msg)

    @client.command(aliases=['list', 'Liste'])
    async def _list(message):
        """
            Listing Current Players. Calls mc_info for Values
        """
        response = mc_info(config.dns_name, int(config.port))
        if response[2] is not None:
            current_players = response[2]
        else:
            current_players = "??"
        if response[3] is None and response[0] is True:
            msg = "This Server does not support the retrieval of player names (Query might be disabled). Use `!mc` or `!status` for more server info."
        elif response[3] is None and response[0] is False:
            msg = "The Minecraft server is down! ❌"
        else:
            players_names = response[3]
            # ''' makes a Quote in Discord.
            # \n has to be here or discord would suck up the first Value
            msg = "```\n"
            for name in players_names:
                msg += name + "\n"
            msg += "```"
            if current_players == 0:
                msg = "Unfortunately, no one is online at the moment 😢"
        await message.send(msg)

    @client.command(aliases=['help', 'Help'])
    async def _help(message):
        """
            Help Command using embeds to make it look ok
        """
        embed = discord.Embed(title="Minecraft Server Observer", description="Commands:", color=0xeeF657)

        embed.add_field(name="#hello", value="Says hello", inline=False)
        embed.add_field(name="#mc or #status", value="Checks the server status", inline=False)
        embed.add_field(name="#list", value="lists the current online players", inline=False)
        #embed.add_field(name="#lastonline", value="checks who was last to leave the server, not programmed atm", inline=False)
        embed.add_field(name="#info", value="Gives a little info about the bot", inline=False)
        embed.add_field(name="#help", value="Gives this message", inline=False)

        await message.send(embed=embed)

    @client.command(aliases=['mc', 'minecraft', 'Minecraft', 'status', 'Status', 'up'])
    async def _mc(message):
        await message.send("Fetching Server Status")
        response = mc_info(config.dns_name, int(config.port))
        if response[0]:
            if response[1] is not None:
                ip = response[1]
            else:
                ip = "??"
            if response[2] is not None:
                current_players = response[2]
            else:
                current_players = "??"

            if response[3] is not None:
                players_names = "```\n"
                for name in response[3]:
                    players_names += name + "\n"
                players_names += "```"
                if current_players == 0:
                    players_names = ""
            else:
                players_names = ""
        
            if ip is not None:
                name = name + " (" + ip + ")"
    
            if response[4] is not None:
                software = response[4]
            else:
                software = "??"
    
            if response[5] is not None:
                version = response[5]
            else:
                version = "??"
    
            if response[6] is not None:
                motd = response[6]
            else:
                motd = config.dns_name

            if response[7] is not None:
                #Implement last_online for when nobody is online. But idk, Do you need that?
                #TODO maybe...
                last_online = response[7]
            else:
                last_online = "??"

            if response[8] is not None:
                #TODO remove the DOT and 0 from the Ping so it looks nicer
                latency = round(float(response[8]), 0)
            else:
                latency = "??"

            if response[9] is not None:
                maps = response[9]
            else:
                maps = "??"

            if response[10] is not None:
                dns_name = response[10]
            else:
                dns_name = "??"
            if response[11] is not None:
                max_players = response[11]
            else:
                max_players = "??"

            #The | makes it look nicer for some reason. Not so squished. Prob the Width of a emoticon
            #is very small, causing the other embed to clip into it a bit.
            # Looks like shit on mobile lol
            if response[2] == 0:
                #TODO If no one is online, show last_online
                players_online = "No one is online at the moment,last Online {0} 😢|".format(last_online)
            elif response[2] == 1:
                players_online = "There is one player online 😃|"
            elif response[2] > 1:
                players_online = "There are {0} players online 😃|".format(current_players)      
            
            status = "{0} is up! ✅".format(dns_name)
        else:
            status = "The Minecraft server is down! ❌"
            players_online = ""
            players_names = ""
            name = config.server_name
            latency = "??"
            ip = "??"
        embed = discord.Embed(colour=discord.Colour(0x80ff), description=status, timestamp=datetime.datetime.utcnow())
        #TODO get favicon( learn wtf favicons are) from server > set static one to github from gewuerzhost
        """if response[0]:
            embed.set_author(name=name, icon_url="http://www.google.com/s2/favicons?domain=" + ip)
        else:
            embed.set_author(name=message_input[1], icon_url="http://www.google.com/s2/favicons?domain=" + message_input[1])
        embed.set_footer(text="Powered by DPMBot", icon_url="{0}".format(config.favicon_github)))
        """
        if current_players != 0:
            embed.add_field(name="Players {0}/{1}".format(current_players, max_players), value=players_online + "\n" + players_names)

        if latency != "??":
            embed.add_field(name="Minecraft Info", value="Ping: {0} ms\nIP: `{1}`\nVersion: `{2}`\nSoftware: `{3}`\nMap: `{4}`".format(latency, ip, version, software, maps), inline=True)

        await message.send(embed=embed)   

    @client.command(aliases=['restart'])
    async def _restart(message):
        """
            Doing a Soft Restart of the Bot, reloading all services
        """
        print("Terminating")
        msg = 'Ok {0.author.mention}, I am Restarting! 👋'.format(message)
        raise SystemExit

def handle_exit():
    """
        Function to handle Exits by taking into account current running loops 
        and trying to wait until they are done(I think)
        Got this from stackexchange.
        https://stackoverflow.com/questions/50957031/how-to-make-discord-py-bot-run-forever-if-client-run-returns
    """
    print("Handling")
    #client.logout forces the bot to reconnect. TODO figure out how to
    # make him not reconnect when the status_task loop fails
    client.loop.run_until_complete(client.logout())
    for t in asyncio.Task.all_tasks(loop=client.loop):
        if t.done():
            t.exception()
            continue
        t.cancel()
        try:
            client.loop.run_until_complete(asyncio.wait_for(t, 5, loop=client.loop))
            t.exception()
        except asyncio.InvalidStateError:
            pass
        except asyncio.TimeoutError:
            pass
        except asyncio.CancelledError:
            pass

async def status_task():
    """
        Loop to change Task acording to Server Status using Asynchronous Commands
    """
    await client.wait_until_ready()
    while True:
        await asyncio.sleep(pingFrequency)
        response = mc_info(config.dns_name, int(config.port))
        if response[0]:
            #not sure how to let it empty or something :D would be smarter to write if respone[0]
            #is not true or something.TODO
            a = "b"
        else:
            await client.change_presence(activity=discord.Game(name=config.server_name + ' is Offline'), status=discord.Status.idle)
            raise SystemExit
            # forcing the loop to restart, not that smooth since the bot will leave the server,
            #TODO Change to a smoother restart. Prob gotta do a double while loop
        if response[2] is not None:
            current_players = response[2]
        else:
            current_players = "??"

        if response[8] is not None:
            latency = round(float(response[8]), 0)
        else:
            latency = "??"

        if response[11] is not None:
            max_players = response[11]
        else:
            max_players = "??"

        if response[2] == 0:
            await client.change_presence(activity=discord.Game(name='{0}/{1} \nPing: {2}'.format(current_players, max_players, latency)), status=discord.Status.idle)
        
        elif response[2] == 1:
            await client.change_presence(activity=discord.Game(name='{0}/{1} \nPing: {2}'.format(current_players, max_players, latency)), status=discord.Status.online)
        
        elif response[2] > 1:
            await client.change_presence(activity=discord.Game(name='{0}/{1} \nPing: {2}'.format(current_players, max_players, latency)), status=discord.Status.online)

@client.event
async def on_ready():
    """
        Gets printed when the Bot logged into the Server and is ready to accept Commands
    """
    logger.info("Logged in as {0} (ID: {1})".format(client.user.name, client.user.id))
    print("Logged in as {0} (ID: {1})".format(client.user.name, client.user.id))
    print('------')
    await client.change_presence(activity=discord.Game(name=config.server_name + ' is Offline'), status=discord.Status.idle)

while True:
    """
        so, the idea is to let the bot restart itself when something goes wrong and it crashed.
        atm it is getting abused to restart the bot when the Server is offline.
        Since for some to me unknown reason the programm loses all client. stuff I added
        (maybe because I set client = again?) I have to call load_functions again
    """
    load_functions()
    #creates a loop task. The loop taks waits around 60 seconds(acc. to ping_frequency)
    client.loop.create_task(status_task())
    try:
        #actually unsure how it "realy" works, but it works? good enough :D
        client.loop.run_until_complete(client.start(TOKEN))
        print("stuff")
    except SystemExit:
        handle_exit()
    except KeyboardInterrupt:
        handle_exit()
        client.loop.close()
        print("Program ended")
        break

    print("Bot restarting")
    client = commands.Bot(command_prefix='#')
