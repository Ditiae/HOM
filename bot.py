# Copyright (c) <2018>, Ethan <ipvedaily@gmail.com>
# Copyright (c) <2018>, Eef Top <eeftop1994@gmail.com>
# Copyright (c) <2018>, L eon <https://github.com/LeonSkills>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import json
import os
import random
import sys
import time
import datetime
import discord

from discord.ext.commands import Bot, CommandNotFound, DisabledCommand, CheckFailure, MissingRequiredArgument, \
    BadArgument, TooManyArguments, UserInputError, CommandOnCooldown
from discord.ext import commands
from discord import Game, Forbidden
from Settings import Settings
from analyzer import Analyzer

VERSION = "1.7.2\n" \
          "Last Updated: 11/1/2018"
BOT_PREFIX = ("~", "?")
client = Bot(command_prefix=BOT_PREFIX)
analyzer = Analyzer(client)
auth_file = 'auth.json'
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
settings = Settings()
start_time = time.time()


class WrongChannelError(commands.CommandError):
    pass


@client.command(name='stats', help="", brief="Shows stats of top 10 scouts.", description="",
                aliases=['highscores'])
@commands.cooldown(rate=1, per=120, type=commands.BucketType.channel)
@commands.has_any_role(*settings.ranks)
async def stats(ctx, arg="scouts"):
    channel = ctx.message.channel
    if channel.name == settings.bot_channel:
        await analyzer.stats(channel, arg)
    else:
        pass


@client.command(name='fullstats', help="", brief="Shows stats of all scouts.", description="",
                aliases=['fullhighsores'])
@commands.cooldown(rate=1, per=600, type=commands.BucketType.channel)
@commands.has_any_role(*settings.ranks)
async def fullstats(ctx, arg="scouts"):
    channel = ctx.message.channel
    if channel.name == settings.bot_channel:
        await analyzer.fullstats(channel, arg)
    else:
        pass


@client.command(name='save', help="", brief="", description="", hidden=True)
@commands.has_any_role(*settings.ranks)
async def save(ctx):
    await analyzer.save()
    await ctx.send("Saving finished.")


@client.command(name='uptime', help="", brief="Displays how long bot has been live.", description="")
async def uptime(ctx):
    channel = ctx.message.channel
    if channel.name == settings.bot_channel:
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=ctx.message.author.top_role.colour)
        embed.add_field(name="Bot Uptime:", value=text)
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + text)
    else:
        pass


@client.command(name='raffle', help='Chooses someone at random to win.', brief="", description="")
@commands.has_role("Staff")
async def raffle(ctx):
    channel = ctx.message.channel
    if channel.name == "scout-raffle":
        await analyzer.raffle(channel)
    else:
        return


@client.command(name='resetweek', help='Resets the week.', brief="", description="")
@commands.has_role("Staff")
async def resetweek(ctx):
    if ctx.message.channel.name == "scout-raffle":
        await analyzer.resetweek()
        await ctx.send("Week reset. Good luck scouts!")
    else:
        return


@client.command(name='entries', help='Displays entries for all weekly scouts.', brief="", description="")
async def entries(ctx):
    channel = ctx.message.channel
    if channel.name == settings.bot_channel:
        await analyzer.entries(channel)
    else:
        return


@client.command(name='ban', help="", brief="Adds username for staff to ban.", description="")
@commands.has_role("Staff")
async def ban(ctx, *names):
    name = ' '.join(names)
    channel = ctx.message.channel
    if channel.name == "ranks-and-bans":
        await analyzer.addban(name, ctx.message.channel)
    else:
        raise WrongChannelError


@client.command(name='rank', help="", brief="Adds username for staff to rank.", description="")
@commands.has_role("Staff")
async def rank(ctx, *names):
    name = ' '.join(names)
    channel = ctx.message.channel
    if channel.name == "ranks-and-bans":
        await analyzer.addrank(name, ctx.message.channel)
    else:
        raise WrongChannelError


@client.command(name='removeban', help="", brief="Removes bans from list.", description="", aliases=['unban', 'deban'])
@commands.has_role("Staff")
async def removeban(ctx, *names):
    name = ' '.join(names)
    channel = ctx.message.channel
    if channel.name == "ranks-and-bans":
        await analyzer.removeban(name, ctx.message.channel)
    else:
        raise WrongChannelError


@client.command(name='removerank', help="", brief="Removes rank from list.", description="",
                aliases=['unrank', 'derank'])
@commands.has_role("Staff")
async def removerank(ctx, *names):
    name = ' '.join(names)
    channel = ctx.message.channel
    if channel.name == "ranks-and-bans":
        await analyzer.removerank(name, ctx.message.channel)
    else:
        raise WrongChannelError


@client.command(name='clearbans', help="", brief="Clears ban list.", description="")
@commands.has_role("Staff")
async def clearbans(ctx):
    channel = ctx.message.channel
    if channel.name == "ranks-and-bans":
        await analyzer.clearbans(ctx.message.channel)
    else:
        raise WrongChannelError


@client.command(name='clearranks', help="", brief="Clears rank list.", description="")
@commands.has_role("Staff")
async def clearranks(ctx):
    channel = ctx.message.channel
    if channel.name == "ranks-and-bans":
        await analyzer.clearranks(ctx.message.channel)
    else:
        raise WrongChannelError


@client.command(name='showbans', help="", brief="Shows just ban list.", description="",
                aliases=['bans'])
@commands.has_role("Staff")
async def showbans(ctx):
    channel = ctx.message.channel
    if channel.name == "ranks-and-bans":
        await analyzer.showbans(channel)
    else:
        raise WrongChannelError


@client.command(name='showranks', help="", brief="Shows just rank list.", description="")
@commands.has_role("Staff")
async def showranks(ctx):
    channel = ctx.message.channel
    if channel.name == "ranks-and-bans":
        await analyzer.showranks(channel)
    else:
        raise WrongChannelError


@client.command(name='show', help="", brief="Shows rank and ban list.", description="")
@commands.has_role("Staff")
async def show(ctx):
    channel = ctx.message.channel
    if channel.name == "ranks-and-bans":
        await analyzer.showranksandbans(channel)
    else:
        raise WrongChannelError


@client.command(name='lookup', help="Can tag someone to lookup specific users stats.", brief="", description="",
                aliases=[''])
async def lookup(ctx):
    channel = ctx.message.channel
    for id in ctx.message.mentions:
        if channel.name == settings.bot_channel:
            await analyzer.lookup(channel, str(id.id))
    else:
        pass


@client.command(name='mystats', help="View your stats.", brief="", description="")
async def mystats(ctx):
    channel = ctx.message.channel
    id = str(ctx.message.author.id)
    if channel.name == settings.bot_channel:
        await analyzer.lookup(channel, id)
    else:
        pass


@client.command(name='slap', help="", brief="", description="")
async def slap(ctx, user):
    channel = ctx.message.channel
    if channel.name == settings.bot_channel:
        await ctx.send(f"{ctx.message.author.name} slapped {user}‽")
    else:
        pass


@client.command(name='resetscout', help="Deletes your assigned scout list.", aliases=['rs'], brief="", description="")
async def resetscout(ctx):
    channel = ctx.message.channel
    if channel.name in settings.channels:
        author = ctx.message.author
        username = author.name
        await analyzer.reset_scout(channel, str(author.id), username)


@client.command(name='mute', help="Mutes the bot from pming you.", brief="", description="",
                aliases=['zipit', 'stfu'])
async def mute(ctx):
    channel = ctx.message.channel
    if channel.name in settings.channels:
        author = ctx.message.author
        username = author.name
        await analyzer.set_mute(channel, str(author.id), username, 1)


@client.command(name='unmute', help="Unmutes the bot so you can be messaged.", brief="", description="",
                aliases=['unzipit'])
async def unmute(ctx):
    channel = ctx.message.channel
    if channel.name in settings.channels:
        author = ctx.message.author
        username = author.name
        await analyzer.set_mute(channel, str(author.id), username, 0)


@client.command(name='updatescoutstats', help="fixes issues with unset scout fields", brief="", description="")
@commands.has_any_role(*settings.ranks)
async def updatescoutstats(ctx):
    channel = ctx.message.channel
    if channel.name in settings.channels:
        await analyzer.update_scout_stats()


@client.command(name='scout', help='Gives you a list of best worlds to scout.', brief="", description="",
                aliases=['request', 'req'])
async def scout(ctx, *args):
    channel = ctx.message.channel
    if len(args) != 0:
        num_worlds = int(args[0])
        if num_worlds < 3:
            await ctx.send("You must request at least 3 worlds.")
            return
    if channel.name == "scouting":
        username = ctx.message.author.name
        author = ctx.message.author
        await analyzer.get_scout_info(channel, author, username, args)


@client.command(name='relay', help="Brings worldlist to newest message.", brief="", description="",
                aliases=['worlds', 'list', 'calls'])
async def relay(ctx):
    channel = ctx.message.channel
    if channel.name in settings.channels:
        await analyzer.relay(channel)


@client.command(name='worldlist', help="Shows all scouted worlds.", brief="", description="")
@commands.cooldown(rate=1, per=180, type=commands.BucketType.channel)
async def worldlist(ctx):
    channel = ctx.message.channel
    if channel.name == "scouting":
        await ctx.send(analyzer.get_table(False))


@client.command(name='deleteworlddata',
                help='Refreshes current world data. If you are found abusing, you will be removed.'
                     ' Works only with Staff rank.', brief="", description="",
                aliases=['deleteeverythingrightmeow'])
@commands.has_any_role(*settings.ranks)
async def deleteworlddata(ctx):
    channel = ctx.message.channel
    possible_replies = [
        'abolished',
        'obliterated',
        'annihilated',
        'eliminated',
        'removed',
        'cleared',
        'erased',
        'emptied',
        'nulled',
        'terminated',
        'eradicated',
        'negated',
        'undone',
        'wiped',
        'destroyed'
    ]
    if channel.name in settings.channels:
        await analyzer.reset()
        response = f"World data has been {random.choice(possible_replies)}."
        await ctx.send(response)
        await analyzer.relay(channel)


@client.command(name='stop', help='Stops bot vigorously. Works only with Staff rank.', brief="", description="")
@commands.has_role("Staff")
async def stop(ctx):
    analyzer.logger.warning("Attempting to stop")
    await analyzer.saves()
    await analyzer.savew()
    await ctx("Stopping....")
    await client.logout()
    exit(0)


@client.command(name='restart', help='Restarts bot.', brief="", description="")
@commands.has_role("Staff")
async def restart(ctx):
    await analyzer.saves()
    await analyzer.savew()
    await ctx.send("Restarting....")
    analyzer.restart_program()


@client.command(name='ping', help='Checks bots ping.', brief="", description="")
async def ping(ctx):
    channel = ctx.message.channel
    if channel.name == settings.bot_channel:
        embed = discord.Embed(colour=ctx.message.author.top_role.colour)
        embed.add_field(name="Pong! :ping_pong:", value="...")
        message = await ctx.send(embed=embed)
        t1 = time.perf_counter()
        await channel.trigger_typing()
        t2 = time.perf_counter()
        pingms = round((t2-t1)*1000)
        embed.set_field_at(0, name="Pong! :ping_pong:", value=f"Pong: {pingms}ms")
        await message.edit(embed=embed)
    else:
        pass


@client.command(name='commands', help='Lists commands for calling/scouting.', brief="Lists commands", description="")
async def commands(ctx):
    channel = ctx.message.channel
    if channel.name == settings.bot_channel:
        await ctx.send("To report on a world: `w[#] [number of active plinths]`.\n"
                         "Example: `w59 4` or `14 2`\n\n"
                         "To call a core: `w[#] [core name]`.\n"
                         "Example: `w12 cres` or `42 seren`.\n"
                         "Aliases for core names are shown here: `['cres', 'c', 'sword', 'edicts', 'e', 'sw', 'juna', "
                         "'j', 'seren', 'se', 'aagi', 'a']`.\n\n"
                         "To delete a world: `w[#] [0, d, dead, or gone]`.\n"
                         "Example: `w103 d` or `56 0`\n\n"
                         "To get a list of worlds to scout: `?scout [optional amount]`. \n"
                         "Example: `?scout` for a default of 10 worlds or `?scout 5` for 5 worlds.\n"
                         "If you dont want/can to complete the list use `?resetscout`.\n"
                         "If you can't do a world just report it to be 0, or ask someone else to do it for you\n"
                         "To disable the bot pming your list of worlds: `?mute`\n"
                         "To enable the bot pming your list of worlds: `?unmute`\n\n"
                         "You can report the worlds in pm to the bot if you want.\n\n"
                         "The next column will display a max of 10 worlds sorted by active plints.\n"
                         "To get the full list: `?worldlist`")
    else:
        pass


@client.command(name='info', help='Lists FC info.', brief="", description="")
async def info(ctx):
    channel = ctx.message.channel
    if channel.name == settings.bot_channel:
        await ctx.send("Look in: #fc-info for information.")
    else:
        pass


@client.command(name='version', help='Lists current bot version.', brief="", description="")
async def version(ctx):
    channel = ctx.message.channel
    if channel.name == settings.bot_channel:
        await ctx.send("Current bot version: " + VERSION)
    else:
        pass


@client.command(name='ranks', help='Lists current FC ranks.', brief="", description="")
async def ranks(ctx):
    channel = ctx.message.channel
    if channel.name == settings.bot_channel:
        rankies = {"6xx\n",
                   "VictoriaKins\n",
                   "WealthRS"}
        rankies = sorted(rankies)
        ranks_str = ""
        for name in rankies:
            ranks_str += str(name)
        await ctx.send("```\n" + ranks_str + "\n```")
    else:
        pass


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="Hall of Memories"))
    await analyzer.loadworlds()
    await analyzer.loadscouts()
    analyzer.logger.info('Connected!')
    analyzer.logger.info('Username: ' + client.user.name)
    analyzer.logger.info('ID: ' + str(client.user.id))
    server = [x for x in client.guilds if x.name == settings.servers][0]
    bot_channel = [x for x in server.channels if x.name == settings.bot_only_channel][0]
    await bot_channel.send("Nobody fear, the bot is here!")


mainMessage = None


@client.event
async def on_message(message):
    # Check if it's not our own message, don't want infinite loops
    if message.author == client.user:
        return

    analyzer.logger.info(f"Received message {message.content} in channel {message.channel} from {message.author.name}"
                         f" at {datetime.datetime.now().strftime('%I:%M%p on %B %d')}".translate(non_bmp_map))
    # Check if we are in the right channel
    if isinstance(message.channel, discord.abc.PrivateChannel):
        # await analyzer.analyze_call(message)
        return

    if message.channel.name not in settings.channels:
        return

    if message.guild.name not in settings.servers:
        return

    message.content = message.content.lower()
    await client.process_commands(message)

    # Analyse the message
    await analyzer.analyze_call(message)


@client.event
async def on_command_error(ctx, error):
    analyzer.logger.error(f"Rip, error {ctx}, {error}")
    errors = {
        CommandNotFound: 'Command not found.',
        DisabledCommand: 'Command has been disabled.',
        CheckFailure: 'Missing required permissions to issue command.',
        MissingRequiredArgument: 'Command missing required arguments.',
        BadArgument: 'Failed parsing given arguments.',
        TooManyArguments: 'Too many arguments given for command.',
        UserInputError: 'User input error.',
        CommandOnCooldown: f'{error}',
        WrongChannelError: 'Command issued in a channel that isn\'t allowed.',
        Forbidden: 'I do not have the correct permissions.'
    }
    for error_type, text in errors.items():
        if isinstance(error, error_type):
            analyzer.ab.notify(error)
            return await ctx.message.channel.send("Command error: " + errors[error_type])

if not os.path.exists(auth_file):
    analyzer.logger.error("no auth json found, please create one")

with open(auth_file) as f:
    auth_data = json.load(f)

# client.run(os.environ['BOTTOKEN'])
client.run(auth_data['token'])
