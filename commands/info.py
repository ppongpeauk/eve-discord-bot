'''
    Filename: info.py
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

class Info(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @cog_ext.cog_slash(
    name="avatar",
    description="display a user's profile picture.",
    options=[
      create_option(
        name="user",
        description="a discord user (defaults to yourself.)",
        option_type=6,
        required=False
      )
    ],
    **command_default
  )
  async def _avatar(self, ctx: SlashContext, user=None):
    get_user = ctx.author if not user else user
    embed = discord.Embed(
      title=f"{get_user.name}'s avatar",
    )
    embed.set_footer(**embed_default["footer"])
    embed.set_image(url=get_user.avatar_url_as(static_format="png"))
    await ctx.send(embed=embed)

  @cog_ext.cog_subcommand(
    base="info",
    name="user",
    description="display info about a discord user.",
    options=[
      create_option(
        name="user",
        description="a discord user (defaults to yourself.)",
        option_type=6,
        required=False
      )
    ],
    **command_default
  )
  async def _user_info(self, ctx: SlashContext, user=None):
    get_user = ctx.author if not user else user
    embed = discord.Embed(
      title=f"about {get_user.name}", color=0xffffff,
    )
    embed.set_footer(**embed_default["footer"])
    # fields!
    embed.add_field(name="name & tag", value=get_user, inline=True)
    embed.add_field(name="server join date", value=get_user.joined_at, inline=True)
    embed.add_field(name="account creation date", value=get_user.created_at, inline=True)
    embed.add_field(name="user id", value=get_user.id, inline=True)
    # user icon
    embed.set_thumbnail(url=get_user.avatar_url_as(static_format="png"))

    await ctx.send(embed=embed)

  @cog_ext.cog_subcommand(
    base="info",
    name="server",
    description="display info about this discord server.",
    **command_default
  )
  async def _server_info(self, ctx: SlashContext):
    if ctx.guild is not None:
      embed = discord.Embed(
        title=f"about {ctx.guild.name}", color=0xffffff,
      )
      embed.set_footer(**embed_default["footer"])
      # fields!
      embed.add_field(name="name", value=ctx.guild.name, inline=True)
      embed.add_field(name="proprietor", value=ctx.guild.owner, inline=True)
      embed.add_field(name="server creation date", value=ctx.guild.created_at, inline=True)
      embed.add_field(name="# of members", value=ctx.guild.member_count, inline=True)
      embed.add_field(name="# of server boosts", value=ctx.guild.premium_subscription_count, inline=True)
      embed.add_field(name="bitrate limit", value=f"{int(ctx.guild.bitrate_limit/1000)} kbps", inline=True)
      embed.add_field(name="server id", value=ctx.guild.id, inline=True)
      # server icon
      embed.set_thumbnail(url=ctx.guild.icon_url_as(static_format="png"))
      # server banner (if applicable)
      embed.set_image(url=ctx.guild.banner_url_as(format="png"))

      await ctx.send(embed=embed)
    else:
      await ctx.send(content="this command isn't being run on a discord guild!")
def setup(bot):
  bot.add_cog(Info(bot))