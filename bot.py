import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from util.HelpCustom import MyHelpCommand
from util.helpers import send_with_mention
from leetcode import check_daily_completion, fetch_daily_problem, fetch_problem_by_difficulty

# get lcb token
load_dotenv()
TOKEN = os.getenv('DISCORD_LCB_TOKEN')

# intents == privs
intents = discord.Intents.default()
intents.message_content = True  # read messages priv
intents.members = True

# create instance
bot = commands.Bot(command_prefix="!", intents=intents, help_command=MyHelpCommand())


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_command_error(ctx, error):
    '''Handles errors for commands that are not used correctly'''
    if isinstance(error, commands.CommandNotFound):
        await send_with_mention(ctx, f"❌ **Invalid command** Type `!help` to see available commands\n{error}")
    elif isinstance(error, commands.MissingRequiredArgument):
        await send_with_mention(ctx, f"❌ **Missing argument** Please provide the correct argument(s)\n{error}")
    elif isinstance(error, commands.BadArgument):
        await send_with_mention(ctx, f"❌ **Bad argument** Input is in wrong format\n{error}")
    else:
        await send_with_mention(ctx, f"❌ **Unknown error** <@{ctx.guild.owner.id}> Fix it\n{error}")

@bot.command(hidden=True)
async def hello(ctx):
    """Responds with a greeting."""
    await ctx.send(f"Hello, {ctx.author.mention}!")

@bot.command()
async def daily(ctx):
    '''Display the daily leetcode problem'''
    daily_problem = await fetch_daily_problem(message_only=True)
    # await ctx.send(daily_problem)
    await send_with_mention(ctx, daily_problem)

@bot.command()
async def check_daily(ctx, username):
    '''Check if <username> completed the daily leetcode question'''
    completed = await check_daily_completion(username)
    # await ctx.send(completed)
    await send_with_mention(ctx, completed)

@bot.command()
async def problem(ctx, difficulty):
    '''Get a random free problem given a difficulty <easy|medium|hard>'''
    valid_difficulties = {"EASY", "MEDIUM", "HARD"}
    difficulty = difficulty.upper()
    if difficulty not in valid_difficulties:
        print('difficulty error')
        raise commands.BadArgument('<difficulty> MUST be "easy", "medium", or "hard"')
    problem = await fetch_problem_by_difficulty(difficulty)
    await send_with_mention(ctx, problem)

bot.run(TOKEN)
