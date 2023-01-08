# import main dependencies
import discord, json, time
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
# import dependencies for commands
import random
import globals
# import settings
settings = None
with open("settings.json", "r") as settings_file:
    settings = json.load(settings_file)

command_default = settings.get("commandDefault")
embed_default = settings.get("embedDefault")

class BotOwner(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @cog_ext.cog_subcommand(
    base="owner",
    name="activity",
    description="change the bot's activity (bot maintainers only)",
    options=[
      create_option(
        name="type",
        description="the desired activity type.",
        option_type=3,
        required=True,
        choices=[
          create_choice(
            name="playing",
            value="playing"
          ),
          create_choice(
            name="listening",
            value="listening"
          ),
          create_choice(
            name="watching",
            value="watching"
          ),
          create_choice(
            name="streaming",
            value="streaming"
          ),
          create_choice(
            name="competing",
            value="competing"
          )
        ]
      ),
      create_option(
        name="name",
        description="the desired name of the activity.",
        option_type=3,
        required=True
      ),
      create_option(
        name="url",
        description="the desired url of the activity (only used for the streaming type.)",
        option_type=3,
        required=False
      ),
    ],
    **command_default
  )
  async def _activity(self, ctx: SlashContext, type, name, url=""):
    if ctx.author.id in settings.get("admins"):
      try:
        activity = None
        if type != "streaming":
          activity = discord.Activity(type=discord.ActivityType[type], name=name)
          await self.bot.change_presence(activity=activity)
        else:
          activity = discord.Streaming(name=name, url=url)
          await self.bot.change_presence(activity=activity)
        globals.activity_object.set_cache(activity)
        embed = discord.Embed(
          description=f"successfully changed the bot's activity!", color=0xffffff,
        )
        embed.set_footer(**embed_default["footer"])
        await ctx.send(embed=embed)
      except Exception as e:
        embed = discord.Embed(
          description=f"there was a problem while trying to change the activity.", color=0xffffff,
        )
        embed.set_footer(**embed_default["footer"])
        await ctx.send(embed=embed)
    else:
      embed = discord.Embed(
        description="access denied. ❌", color=0xfffff,
      )
      embed.set_footer(**embed_default["footer"])
      await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(BotOwner(bot))