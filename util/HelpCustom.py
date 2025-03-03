from discord.ext import commands

from util.helpers import send_with_mention

class MyHelpCommand(commands.DefaultHelpCommand):
    async def send_bot_help(self, mapping):
        '''Customize how bot help is shown'''
        help_message = '# Bot commands:\n'
        for _, commands_list in mapping.items():
            if commands_list:
                for command in commands_list:
                    if command.hidden:
                        continue
                    help_message += f'`!{command.name} {command.signature}`\n'
                    help_message += f'> {command.help}\n\n'
        help_message += '\n**For specific command help, use `!help <command>`.**'
        #css not needed but could be cool eventually
        await send_with_mention(self.context, f'\n{help_message}\n')

    async def send_command_help(self, command):
        '''Customize how command help is shown'''
        help_message = f'\n`!{command.name} {command.signature}`\n'
        help_message += f'> {command.help}\n'
        await send_with_mention(self.context, help_message)