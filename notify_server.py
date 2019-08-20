__version__ = "0.0.5"

#Python Libary
import asyncio
import datetime
import json
import logging
import os
import re
import urllib.request
import traceback
import sys

#Third Party
import discord
from discord.ext import commands
import mcstatus

#Local Config File
if os.path.isfile("config.py"):
    import config # pylint: disable=import-error
# pylint might be annoying here, since he for some reason cant see config
# unsure how to exactly prevent this

#Checking for env Variable to work with Heroku
#Gotta test it with evniron.get default value being the config file.
if os.environ.get('discord_token') is not None:
    discord_token = os.environ.get('discord_token')
    a_certain_user = os.environ.get('a_certain_user')
    dns_name = os.environ.get('dns_name')
    server_name = os.environ.get('server_name')
    port = os.environ.get('port')
    conf_ip = os.environ.get('ip')
    favicon_github = os.environ.get('favicon_github')
else:
    discord_token = config.discord_token # pylint: disable=no-member
    a_certain_user = config.a_certain_user # pylint: disable=no-member
    dns_name = config.dns_name # pylint: disable=no-member
    server_name = config.server_name # pylint: disable=no-member
    port = config.port # pylint: disable=no-member
    conf_ip = config.ip # pylint: disable=no-member
    favicon_github = config.favicon_github # pylint: disable=no-member

client = commands.Bot(command_prefix='#')
logger = logging.getLogger()
handler = logging.FileHandler("dpm_bot.log", mode="a")
formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(ctx)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
# I have actually no clue how this works, but I need to implement logging :D

LINE = '-------------------------'

ping_Frequency = 10 # in Seconds


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    prefixes = ['#']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return '?'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


"""
for later use, adapting changes from
https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be
initial_extensions = ['cogs.simple',
                      'cogs.members',
                      'cogs.owner']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)
"""





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
        server = mcstatus.MinecraftServer(address, int(port))
    try:
        # usually you would use server.Status here, but for some reason it stopped working :D
        # If the recipent Server is sleeping, the ping will Fail! Some Servers do have a feature
        # to wake up when pinged
        info = int(server.ping())
        status = True
        try:
            # See server.query file for info on what information query gives
            query = server.query()
            ip = None
            players_names = query.players.names  # ex ['user1','user2','user2']
            players_online = query.players.online
            players_max = query.players.max
            last_online = None
            try:
                software = query.software.brand  # ex. Vanilla
                version = query.software.version  # ex. 1.14
                description = query.motd
                maps = query.map
                latency = str(info)
                latency = latency.rstrip('0')
               # latency = info
                latency = re.sub("\.", "", latency)
            except Exception:
                software = None
                version = None
                description = None
                latency = None
                maps = None
                ip = None
                address = None
                players_max = None
                last_online = None
                logger.info('Could not set variables after Query',
                            exc_info=True)
        except Exception:
            players_online = query.players.online
            players_names = None
            logger.info('Server Ping works, but Query Failed', exc_info=True)
    except Exception:
        # to make sure nothing is called that hasn't been set before
        print("status Failed!")
        status = False
        players_online = None
        players_names = None
        software = None
        version = None
        ip = None
        description = None
        latency = None
        maps = None
        address = None
        players_max = None
        last_online = ["", "", "", ""]
        logger.info('Server Down, Status Ping Failed', exc_info=True)
    # Logging threw an error here, so I gotta check it up again.
    #logger.info(status, ip, players_online, players_names, software, version, description, last_online, latency, maps, address, players_max)
    return (status, ip, players_online, players_names,
                software, version, description, last_online, latency, maps, address, players_max)


def load_functions():
    """
        Here are serveval Decorators using Discord.py to react to Commands in Chat.
        for Example > #hello in chat would trigger @client.command and do whatever _hello is.

    """
    client.remove_command('help')

    @property
    def version(self):
        return __version__

    @client.command(aliases=['hello', 'Hello', 'Hi', 'hi'])
    async def _hello(ctx: str.lower):
        """
            Command to say something and mention the author who asked.
        """
        msg = 'Hello {0.author.mention}! 👋'.format(ctx)
        await ctx.send(msg)

    @client.command(aliases=['stop', 'Stop'])
    @commands.is_owner()
    async def _stop(ctx: str.lower):
        """
            Raising a keyboardInterrupt and not SystemExit
            , because we catch both but t urn SystemExit
            into a Restart of the Bot, while KeyboardInterrupt stops it
            This is Abuseable, should probl remove once you are
            done testing, or something.
        """
        msg = 'Byyyyyiiiee {0.author.mention}, 👋'.format(ctx)
        await ctx.send(msg)
        raise KeyboardInterrupt

    @_stop.error
    async def _stop_handler(ctx,):
        await ctx.send("You are not allowed to use the Command Stop")

    @client.command(aliases=['shhhh'])
    async def _shutup(ctx: str.lower):
        """
            A command for a certain human being who thinks this bot
            is being abused...
        """
        msg = '''Thank you my godemporer {0.author.mention},
            I hereby order @{1} to shut the fuck up,
            I am here of Free Will! 👋'''.format(ctx, a_certain_user) # pylint: disable=no-member
        await ctx.send(msg)

    @client.command(aliases=['info', 'information'])
    async def _info(ctx: str.lower):
        """
            Info Command giving out the Code Source
        """
        # TODO Figure out how to make it a direct link, not sure if this works atm
        msg = 'For More information regarding this bot, visit https://github.com/Iphex/DPMBot'
        await ctx.send(msg)

    @client.command(aliases=['list', 'Liste'])
    async def _list(ctx: str.lower):
        """
            Listing Current Players. Calls mc_info for Values
        """
        # TODO embed current / max players
        response = mc_info(dns_name, int(port)) # pylint: disable=no-member
        if response[2] is not None:
            current_players = response[2]
        else:
            current_players = "??"
        if response[3] is None and response[0] is True:
            msg = """This Server does not support the retrieval of player names
             (Query might be disabled). Use `!mc` or `!status` for more server info."""
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
        await ctx.send(msg)

    @client.command(aliases=['help', 'Help'])
    async def _help(ctx: str.lower):
        """
            Help Command using embeds to make it look ok
        """
        embed = discord.Embed(
            title="Minecraft Server Observer",
            description="Commands:",
            color=0xeeF657)

        embed.add_field(
            name="#hello",
            value="Says hello",
            inline=False)
        embed.add_field(
            name="#mc or #status",
            value="Checks the server status",
            inline=False)
        embed.add_field(
            name="#list",
            value="lists the current online players",
            inline=False)
        # embed.add_field(
        #   name="#lastonline",
        #   value="checks who was last to leave the server, not programmed atm",
        #   inline=False)
        embed.add_field(
            name="#info",
            value="Gives a little info about the bot",
            inline=False)
        embed.add_field(
            name="#help",
            value="Gives this ctx",
            inline=False)
        await ctx.send(embed=embed)

    @client.command(
        aliases=['mc', 'minecraft', 'Minecraft', 'status', 'Status', 'up'])
    async def _mc(ctx: str.lower):
        await ctx.send("Fetching Server Status")
        response = mc_info(dns_name, int(port))
        if response[0]:
            ip = conf_ip
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
                motd = dns_name # pylint: disable=no-member

            if response[7] is not None:
                # Implement last_online for when nobody is online.
                # But idk, Do you need that?
                # TODO maybe...
                last_online = response[7]
            else:
                last_online = "??"

            if response[8] is not None:
                # TODO remove the DOT and 0 from the Ping so it looks nicer
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
                # TODO If no one is online, show last_online
                players_online = "No one is online at the moment"
                # players_online = "No one is online at the moment,last Online {0}
                # 😢".format(last_online)
            elif response[2] == 1:
                players_online = "There is one player online 😃"
            elif response[2] > 1:
                players_online = "There are {0} players online 😃".format(
                    current_players)

            status = "{0} is up! ✅".format(dns_name)
        else:
            #TODO see if any of this is needed / unneeded
            status = "The Minecraft server is down! ❌"
            players_online = "??"
            players_names = "??"
            software = "??"
            current_players = 0
            max_players = 12
            dns_name = "??"
            maps = "??"
            version = "??"
            motd = dns_name # pylint: disable=no-member
            last_online = "??"
            name = server_name # pylint: disable=no-member
            latency = "??"
            ip = "??"
        try:
            embed = discord.Embed(
                colour=discord.Colour(0x80ff),
                description=status,
                timestamp=datetime.datetime.utcnow())
            embed.set_footer(
                text="Powered by DPMBot",
                icon_url="{0}".format(favicon_github)) # pylint: disable=no-member
            if current_players != 0:
                # add minimum 5 spaces, and after that according to number of players.
                embed.add_field(
                    name="Players {0} / {1}".format(current_players, max_players),
                    value=players_names + "\n")
                # TODO looks like shit on mobile...
                #embed.add_field(name="|", value=add_spaces(current_players))
            else:
                embed.add_field(
                    name="Players {0} / {1}".format(current_players, max_players),
                    value=players_online + "\n")

            if latency != "??":
                embed.add_field(
                    name="Minecraft Info",
                    value="Ping: {0} ms\nIP: `{1}`\nVersion: `{2}`\nSoftware: `{3}`\nMap: `{4}`"
                    .format(latency, ip, version, software, maps),
                    inline=False)
            else:
                embed.add_field(
                    name="Minecraft Info",
                    value="Offline",
                    inline=False)
        except Exception:
            logger.error('Couldnt Embed', exc_info=True)
            embed = discord.Embed(
                colour=discord.Colour(0x80ff),
                description=status,
                timestamp=datetime.datetime.utcnow())
            embed.add_field(
                name="Players {0}/{1}".format(current_players, max_players),
                value=players_online + "\n")

        await ctx.send(embed=embed)

    @client.command(aliases=['restart'])
    async def _restart(ctx: str.lower):
        """
            Doing a Soft Restart of the Bot, reloading all services
        """
        print("Terminating")
        msg = 'Ok {0.author.mention}, I am Restarting! 👋'.format(ctx)
        raise SystemExit

    @client.event
    async def on_resumed():
        print('reconnected')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.UserInputError)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'{ctx.command} can not be used in Private ctxs.')
            except:
                pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                return await ctx.send('I could not find that member. Please try again.')

       # print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
       #Prints way to much atm :D  traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)"""


def add_spaces(amount):
    """
        should only work if more then 6 Players are there,
        to make sure the embed looks good(still looks shit on mobile).
    """
    spaces = "\t|\n\t|\n\t|\n\t|\n\t|\n"
    i = 6
    amount = int(amount)
    while i <= amount:
        spaces += "\t|\n"
    return spaces


def handle_exit():
    """
        Function to handle Exits by taking into account current running loops
        and trying to wait until they are done(I think)
        Got this from stackexchange.
        https://stackoverflow.com/questions/50957031/
        how-to-make-discord-py-bot-run-forever-if-client-run-returns
    """
    print("Handling")
    # client.logout forces the bot to reconnect. TODO figure out how to
    # make him not reconnect when the status_task loop fails
    client.loop.run_until_complete(client.logout())
    for t in asyncio.Task.all_tasks(loop=client.loop):
        if t.done():
            t.exception()
            continue
        t.cancel()
        try:
            client.loop.run_until_complete(
                asyncio.wait_for(t, 5, loop=client.loop))
            # testing gather all tasks. might work the same as wait_for
            t.exception()
        except asyncio.InvalidStateError:
            pass
        except asyncio.TimeoutError:
            pass
        except asyncio.CancelledError:
            logger.debug('All Pending task have been cancelled')
            pass


def convert(list):
    """returns a tuple when given a list..."""
    return tuple(i for i in list)


"""
def load_files():
        Implement folder loading for future proof.
        TODO gotta first turn the load stuff into a class
    for file in os.listdir('cogs'):
        if not file.endswith('.py'):
            continue
        cog = f'cogs.{file[:-3]}'
        logger.info(info(f'Loading {cog}'))
        try:
            #self.load_extension(cog)
        except Exception:
            logger.exception(f'Failed to load {cog}')
"""

async def status_task():
    """
        Loop to change Task acording to Server Status using Asynchronous Commands
    """
    await client.wait_until_ready()
    while True:
        await asyncio.sleep(ping_Frequency)
        response = mc_info(dns_name, port) # pylint: disable=no-member
        try:
            if response[0] is False:
                await client.change_presence(
                    activity=discord.Game(
                        name=server_name + ' is Offline'),  # pylint: disable=no-member
                    status=discord.Status.dnd)
                print("Response is not true")
                continue
            else:
                try:
                    if response[2] is not None:
                        current_players = response[2]
                    else:
                        current_players = "??"

                    if response[8] is not None:
                        latency = response[8]
                    else:
                        latency = "??"

                    if response[11] is not None:
                        max_players = response[11]
                    else:
                        max_players = "??"
                except Exception:
                    current_players = "??"
                    latency = "??"
                    max_players = "??"
                    logger.info('Server Down', exc_info=True)
                    continue

                if current_players == 0:
                    await client.change_presence(
                        activity=discord.Game(
                            name='{0}/{1} \nPing: {2}'.format(current_players, max_players, latency)),
                        status=discord.Status.idle)

                elif current_players >= 1:
                    await client.change_presence(
                        activity=discord.Game(
                            name='{0}/{1} \nPing: {2}'.format(current_players, max_players, latency)),
                        status=discord.Status.online)

                 #do a lot of stuff
        except Exception as e:
            print("exception", e)
            #raise SystemExit
            # forcing the loop to restart, not that smooth since the bot will leave the server,
            # TODO Change to a smoother restart. Prob gotta do a double while loop

@client.event
async def on_ready():
    """
        Gets printed when the Bot logged into the Server and is ready to accept Commands
    """
    logger.info(LINE)
    print("Logged in as {0} (ID: {1})".format(
        client.user.name, client.user.id))
    logger.info("Logged in as {0} (ID: {1})".format(
        client.user.name, client.user.id))
    await client.change_presence(
        activity=discord.Game(
            name=server_name + ' is Offline'), # pylint: disable=no-member
        status=discord.Status.dnd)

load_functions()
while True:
    """
        so, the idea is to let the bot restart itself when something goes wrong and it crashed.
        atm it is getting abused to restart the bot when the Server is offline.
        Since for some to me unknown reason the programm loses its Client connection. stuff I added
        (maybe because I set client = again?) I have to call load_functions again

        After more researching I found that the bot can restart itself...
    """
    # creates a loop task. The loop taks waits around 10 seconds(acc. to ping_Frequency)
    client.loop.create_task(status_task())
    try:
        # actually unsure how it "realy" works, but it works? good enough :D
        client.loop.run_until_complete(client.start(discord_token, bot=True, reconnect=True))
    # except discord.LoginFailure:
    # this might create a bug unsure tho :(
    #    logger.critical('Invalid token')
    except SystemExit:
        handle_exit()
    except KeyboardInterrupt:
        handle_exit()
        client.loop.close()
        logger.info(LINE)
        logger.info('Shutting Down DPMBot')
        logger.info(LINE)
        break

    print("Bot restarting")
    logger.info(LINE)
    logger.info(f'v{__version__}')
    logger.info(LINE)
    client = commands.Bot(command_prefix='#')
    load_functions()

print("Broke out of while True chain")
