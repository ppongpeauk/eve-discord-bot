'''
    Filename: basic.py
    Author: @restrafes, @evestrafes
    Date Created: 4/5/2021
    Python Version: 3.7.9
'''
# import main dependencies
import discord, json, time
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
# import dependencies for commands
import random
# import settings
settings = None
with open("settings.json", "r") as settings_file:
    settings = json.load(settings_file)

command_default = settings.get("commandDefault")
embed_default = settings.get("embedDefault")

class Basic(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @cog_ext.cog_slash(name="ping", description="report eve's latency.", **command_default) 
  async def _ping(self, ctx: SlashContext):
      time_1 = time.perf_counter()
      await self.bot.fetch_channel(ctx.channel.id)
      time_2 = time.perf_counter()
      ping = round((time_2 - time_1) * 1000)
      await ctx.send(content=f"{random.choice(['hello!', 'howdy!', 'greetings!', 'bonjour!', 'gutentag!', 'hola!'])} **({ping} ms)**")
      
  @cog_ext.cog_slash(
    name="roll",
    description="roll a number between 1-6 (or whichever number(s) you choose.)",
    options=[
      create_option(
        name="min",
        description="minimum number (defaults to 1.)",
        option_type=4,
        required=False
      ),
      create_option(
        name="max",
        description="maximum number (defaults to 6.)",
        option_type=4,
        required=False
      )
    ],
    **command_default
  )
  async def _roll(self, ctx: SlashContext, min=1, max=6):
    try:
      random.seed()
      await ctx.send(content=f"i chose **{str(random.randint(int(min), int(max)))}**!")
    except:
      await ctx.send(content=f"it seems that you've chosen a min. number above 6 without providing a max. number! either enter a valid max. number or choose a min. number below 6!")

def setup(bot):
  bot.add_cog(Basic(bot))