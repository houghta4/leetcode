import os
from database.db import Database
from dotenv import load_dotenv
import discord
from discord.ext import commands
from util.HelpCustom import MyHelpCommand
from util.helpers import send_with_mention, display_db_table
from leetcode import check_daily_completion, fetch_daily_problem, fetch_problem_by_difficulty

# get lcb token
load_dotenv()
TOKEN = os.getenv('DISCORD_LCB_TOKEN')

# intents == privs
intents = discord.Intents.default()
intents.message_content = True  # read messages priv
intents.members = True

# create instance
bot = commands.Bot(command_prefix='!', intents=intents, help_command=MyHelpCommand())

db = Database()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    '''Handles errors for commands that are not used correctly'''
    if isinstance(error, commands.CommandNotFound):
        await send_with_mention(ctx, f'❌ **Invalid command** Type `!help` to see available commands\n{error}')
    elif isinstance(error, commands.MissingRequiredArgument):
        await send_with_mention(ctx, f'❌ **Missing argument** Please provide the correct argument(s)\n{error}')
    elif isinstance(error, commands.BadArgument):
        await send_with_mention(ctx, f'❌ **Bad argument** Input is in wrong format\n{error}')
    elif isinstance(error, discord.Forbidden):
        await send_with_mention(ctx, '❌ **Forbidden** Invalid permissions to assign role\n{error}')
    elif isinstance(error, discord.HTTPException):
        await send_with_mention(ctx, f'❌ **HTTPException** Error assigning role\n{error}')
    else:
        await send_with_mention(ctx, f'❌ **Unknown error** <@{ctx.guild.owner.id}> Fix it\n{error}')

@bot.command(hidden=True)
async def hello(ctx):
    '''Responds with a greeting.'''
    await ctx.send(f'Hello, {ctx.author.mention}!')

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
    valid_difficulties = {'EASY', 'MEDIUM', 'HARD'}
    difficulty = difficulty.upper()
    if difficulty not in valid_difficulties:
        raise commands.BadArgument('<difficulty> MUST be "easy", "medium", or "hard"')
    problem = await fetch_problem_by_difficulty(difficulty)
    await send_with_mention(ctx, problem)

#TODO: make this private so nobody can call this
@bot.command(hidden=True)
async def display_users(ctx):
    '''Display all users in a table format. Should only be used by me or the scheduled job'''
    users = db.get_all_users()

    if not users:
        raise Exception('No users found')
    
    msg = display_db_table(db, 'users')
    await send_with_mention(ctx, f'\n{msg}\n')

#TODO: do i even need notify? just use role
@bot.command()
async def leetcode(ctx, leetcode_username: str = None):
    ''' Toggle `leetcode` role that will add you to list of participating members. 
        - MUST supply leetcode username on first use
        - subsequent uses of `!leetcode` will toggle the role. 
        - `!leetcode <username>` will update your leetcode username '''
    msg = ''
    discord_id = ctx.author.id
    discord_username = ctx.author.name
    role_name = 'leetcoder'
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role is None:
        raise Exception('Could not find `{role_name}`')
    embed = None

    user = db.get_user(discord_id)
    if user:
        print('user is true')
        # existing user
        _, _, _, _, notify, _ = user
        if leetcode_username:
            # update existing user's username. if user doesn't have role, add it
            db.set_leetcode_username(discord_id, leetcode_username)
            msg += f' Leetcode username updated to `{leetcode_username}`'
            if role not in ctx.author.roles:
                db.set_notify(discord_id, True)
                # add role
                await ctx.author.add_roles(role)
                embed = discord.Embed(
                    title="Role added",
                    description=f"You now have the `{role_name}` role.",
                    color=role.color
                )
            
        else:
            # toggle notify in db and add/remove role
            print('leetcode_username = False')
            db.set_notify(discord_id, not bool(notify))
            if role in ctx.author.roles:
                # remove the role
                await ctx.author.remove_roles(role)
                embed = discord.Embed(
                    title="Role removed",
                    description=f"You no longer have the `{role_name}` role.",
                    color=discord.Color.red()
                )
            else:
                # add role
                await ctx.author.add_roles(role)
                embed = discord.Embed(
                    title="Role added",
                    description=f"You now have the `{role_name}` role.",
                    color=role.color
                )
    else:
        if not leetcode_username:
            await send_with_mention(ctx, f'❌ **Must supply leetcode username on first use**')
            return
        # add role
        await ctx.author.add_roles(role)
        embed = discord.Embed(
            title="Role added",
            description=f"You now have the `{role_name}` role.",
            color=role.color
        )
        db.add_user(discord_id, discord_username, leetcode_username)
        msg += f'Leetcode username set to `{leetcode_username}`'
    
    await send_with_mention(ctx, msg, embed=embed)

bot.run(TOKEN)
