# Work with Python 3.7

import datetime
import json
import logging
import urllib.request
import os
import asyncio
import mcstatus
import discord
from discord.ext import commands
import tokens

#Using Discord.py REWRITE
#Using Code from Danny bot, have to rewrite for better performance and readability


TOKEN = tokens.discord_token
client = commands.Bot(command_prefix='#')
client.remove_command('help')

logger = logging.getLogger()
handler = logging.FileHandler("gewuerz_bot.log", mode="a")
formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
pingFrequency = 60
"""
class BotClient(discord.client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)"""


"""
    Referenz > https://github.com/tech189/danny-bot/blob/master/danny-bot.py
    query = server.query()
    print("The server has the following players online: {0}".format(", ".join(query.players.names)))

    print now.strftime("%Y-%m-%d %H:%M")
"""

"""def getServerStatus():
    mcstatus(settings.ip, settings.port)
"""
def mc_info(address, port):
    #TODO don't hardcode server & ip
    info = None
    if port is None:
        print("No Port specified using standard 25565")
        server = mcstatus.MinecraftServer.lookup(address)
    else:
        #server = mcstatus.MinecraftServer.lookup(address + ":" + port)
        server = mcstatus.MinecraftServer(address, port)
    #hwinfo_log = "/media/winshare/hwinfo.CSV"
    mc_log = 'D:\\AMPDatastore\\Instances\\1-Gewuerzhost\\Minecraft\\logs\\latest.log'
    if tokens.server_name_no_caps in address:
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
        #print("printing info before server.status")
        info = server.ping()
        #print("The server replied in {0} ms".format(info))
        status = True
        #testing outputs
        try:
            #testing out what exactly is inside query.version
            query = server.query()
            players_names = query.players.names
            players_online = query.players.online
            players_max = query.players.max
            try:
                #mixed = str(query.version).split()
                software = query.software.brand
                version = query.software.version
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
    #if software == "vanilla":
    #for item in query.raw:
    #    print("item>", item)
    try:
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
            #print(mc_log)
            with open(mc_log, mode="r", encoding="utf-8") as file:
                #print("opened mc_log")
                for line in file:
                    if line[11:58] == "[Server thread/INFO]: Starting Minecraft server":
                        time_started = line[1:9]
            with open(mc_log, mode="r", encoding="utf-8") as file:
                #print("opened mc_log")
                #line_number = 0
                for line in file:
                    #line_number += 1
                    if line[11:33] == "[Server thread/INFO]: " and line[-15:] == " left the game\n":
                        last_player = line[33:-15]
                        last_time = line[1:9]
        #print(old_log, time_started, last_player, last_time)
        last_online = [old_log, time_started, last_player, last_time]
    except:
        last_online = ["", "", "", ""]
    #logger.info("status, ip, players_online, players_names, software, version, description, last_online")
    #logger.info(status, ip, players_online, players_names, software, version, description, last_online)
    return status, ip, players_online, players_names, software, version, description, last_online, latency, maps, address, players_max
"""
def get_statuses():
    fname = "statuses.json"
    if os.path.isfile(fname):
        pass
    else:
        with open(fname, "a") as file:
            file.write("{\"with humans\": \"tech189#0249\"}")
    with open(fname) as file:
        status_dict = json.load(file)

    status_list = []
    for a in status_dict.keys():
        status_list.append(a)
    
    return status_list
"""

def load_stuff():
# Getting All Commands, rewritten for discord.py 1.0.1

    @client.command(aliases=['hello', 'Hello', 'Hi', 'hi'])
    async def _hello(message):
        msg = 'Hello {0.author.mention}! 👋'.format(message)
        await message.send(msg)

    @client.command(aliases=['stop', 'Stop'])
    async def _stop(message):
        msg = 'Byyyyyiiiee {0.author.mention}, 👋'.format(message)
        await message.send(msg)
        raise KeyboardInterrupt

    @client.command(aliases=['shhhh'])
    async def _shutup(message):
        msg = 'Thank you my godemporer {0.author.mention}, I hereby order <@265568746595287051> to shut the fuck up, I am here of Free Will! 👋'.format(message)
        await message.send(msg)

    @client.command(aliases=['list', 'Liste'])
    async def _list(message):
        response = mc_info(tokens.dns_name, int(tokens.port))
        if response[3] is None and response[0] is True:
            msg = "This modded server does not support the retrieval of player names. Use `!mc` or `!status` for more server info."
        elif response[3] is None and response[0] is False:
            msg = "The Minecraft server is down! ❌"
        else:
            players_names = response[3]
            msg = "```\n"
            for name in players_names:
                msg += name + "\n"
            msg += "```"
            if msg == "``````":
                msg = "Unfortunately, no one is online at the moment 😢"
        await message.send(msg)

    @client.command(aliases=['help', 'Help'])
    async def _help(message):
        embed = discord.Embed(title="Simple Minecraft Observer", description="Very Simple:", color=0xeee657)

        embed.add_field(name="#hello", value="Says hello", inline=False)
        embed.add_field(name="#mc or #status", value="Checks the server status", inline=False)
        embed.add_field(name="#list", value="lists the current online players, not programmed atm", inline=False)
        embed.add_field(name="#lastonline", value="checks who was last to leave the server, not programmed atm", inline=False)
        #embed.add_field(name="$info", value="Gives a little info about the bot, not implemented yet", inline=False)
        embed.add_field(name="#help", value="Gives this message", inline=False)

        await message.send(embed=embed)

    @client.command(aliases=['mc', 'minecraft', 'Minecraft', 'status', 'Status', 'up'])
    async def _mc(message):
        await message.send("Fetching Server Status")
        response = mc_info(tokens.dns_name, int(tokens.port))
        #for item in enumerate(response):
        #    print(item)
        # Testing output
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
                if players_names == "``````":
                    players_names = ""
            else:
                players_names = ""

            if response[6] is None:
                try:
                    name = response[1]
                except:
                    name = tokens.dns_name
            else:
                try:
                    name = response[6] + " (" + response[1] + ")"
                except:
                    name = response[6] + tokens.dns_name
        
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
                motd = "??"

            if response[7] is not None:
                last_online = response[7]
            else:
                last_online = "??"

            if response[8] is not None:
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

            if response[2] == 0:
                players_online = "No one is online at the moment 😢         |"
            elif response[2] == 1:
                players_online = "There is one player online 😃         |"
            elif response[2] > 1:
                players_online = "There are {0} players online 😃           |".format(response[2])      
            
            status = "{0} is up! ✅".format(dns_name)
        else:
            status = "The Minecraft server is down! ❌"
            players_online = ""
            players_names = ""
            #TODO another not to be hardcoded, this should be the message_input
            name = tokens.server_name
            latency = "??"
            ip = "??"
        # Gotta add the actual Server name here or for status itself too
        embed = discord.Embed(colour=discord.Colour(0x80ff), description=status, timestamp=datetime.datetime.utcnow())
        #TODO get favicon from server > set static one to github from gewuerzhost
        """if response[0]:
            embed.set_author(name=name, icon_url="http://www.google.com/s2/favicons?domain=" + ip)
        else:
            embed.set_author(name=message_input[1], icon_url="http://www.google.com/s2/favicons?domain=" + message_input[1])
        embed.set_footer(text="Souped up by Danny Bot", icon_url="https://raw.githubusercontent.com/tech189/danny-bot/master/logo.png")
        """
        if players_online != "":
            embed.add_field(name="Players {0}/{1}".format(current_players, max_players), value=players_online + "\n" + players_names)
        if latency != "??":
            embed.add_field(name="Minecraft Info", value="Ping: {0} ms\nIP: `{1}`\nVersion: `{2}`\nSoftware: `{3}`\nMap: `{4}`".format(latency, ip, version, software, maps), inline=True)

        await message.send(embed=embed)   
    """
    @client.command()
    async def on_message(message):
    """

    @client.command(aliases=['restart'])
    async def _restart(message):
        """
            Doing a Soft Restart of the Bot, reloading all services
        """
        print("Terminating")
        msg = 'Ok {0.author.mention}, I am Restarting! 👋'.format(message)
        raise SystemExit

def handle_exit():
    print("Handling")
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
        response = mc_info(tokens.dns_name, int(tokens.port))
        if response[0]:
            #not sure how to let it empty or something :D 
            a = "b"
        else:
            await client.change_presence(activity=discord.Game(name=tokens.server_name + ' is Offline'), status=discord.Status.idle)

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

while True:
    client.remove_command('help')
    load_stuff()
    client.loop.create_task(status_task())
    try:
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
#client.run(TOKEN)
