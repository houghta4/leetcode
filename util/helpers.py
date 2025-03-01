async def send_with_mention(ctx, msg, **kwargs):
    '''Helper to mention sender. Coudln't find default discord way to do it'''    
    await ctx.send(f'{ctx.author.mention} {msg}', **kwargs)