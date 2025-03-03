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
