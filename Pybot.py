import os
import discord
from discord.ext import commands
import sys
from io import StringIO

TOKEN = os.getenv('DISCORD_TOKEN')
BOT = commands.Bot(command_prefix=("PY.", 'Py.','pY.','py.'), case_insensitive= True)

@BOT.event
async def on_ready():
    print(f"{BOT.user.name} has connected to Discord.")

@BOT.command(name="purge") 
async def purge(ctx, num_messages: int):
    channel = ctx.message.channel
    await ctx.message.delete()
    await channel.purge(limit=num_messages, check=None, before=None)

@BOT.listen('on_message')
async def execute(message):
    if message.content.startswith('```python\n') and message.content.endswith('\n```'):
        codeblock = message.content
        
        def formatter(code: str):
            dummy = code.splitlines()
            return "\n".join(dummy[1:-1])
        
        output = StringIO()
        sys.stdout = output
        sys.stderr = output

        try: exec(formatter(codeblock))
        except Exception as e: print(e)
        finally: await message.channel.send(output.getvalue())

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

BOT.run(TOKEN)