import discord


async def send_with_mention(ctx, msg='', **kwargs):
    '''Helper to mention sender. Coudln't find default discord way to do it'''    
    await ctx.send(f'{ctx.author.mention} {msg}', **kwargs)

#TODO: display in a nice format possibly using css
def display_db_table(db, table):
    cols = db.get_columns(table)
    data = db.get_all_table(table)
    
    if not data:
        raise Exception('Error in db.get_all_table({table})')
    
    table_str = '\t '.join(cols)

    for d in data:
        row_str = '\t '.join(str(i) for i in d)
        table_str += f'\n {row_str}'

    return table_str

async def toggle_discord_role(ctx, role_name):
    # toggle role

    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role is None:
        raise Exception('Could not find `{role_name}`')
    
    res = None
    if role in ctx.author.roles:
        # remove the role
        res = await remove_discord_role(ctx, role_name)
    else:
        # add role
        res = await add_discord_role(ctx, role_name)

    return res

async def remove_discord_role(ctx, role):
    # remove role     
    await ctx.author.remove_roles(role)
    return discord.Embed(
        title="Role removed",
        description=f"You no longer have the `{role.name}` role.",
        color=discord.Color.red()
    )

async def add_discord_role(ctx, role):
    await ctx.author.add_roles(role)
    return discord.Embed(
        title="Role added",
        description=f"You now have the `{role.name}` role.",
        color=role.color
    )