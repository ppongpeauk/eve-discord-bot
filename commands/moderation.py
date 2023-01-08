# import main dependencies
import discord, json, time, asyncio
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

class Moderation(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @cog_ext.cog_slash(
    name="nickname",
    description="change a user's nickname (requires 'change nickname' permissions.)",
    options=[
      create_option(
        name="user",
        description="a discord user.",
        option_type=6,
        required=True
      ),
      create_option(
        name="nickname",
        description="the desired nickname (defaults to none.)",
        option_type=3,
        required=False
      ),
    ],
    **command_default
  )
  async def _nickname(self, ctx: SlashContext, user, nickname=None):
    if ctx.author.guild_permissions >= user.guild_permissions and ctx.author.guild_permissions.change_nickname:
      try:
        await user.edit(nick=nickname)
        embed = discord.Embed(
          description=f"successfully changed {user.name}'s nickname to **{str(nickname)}**!", color=0xffffff,
        )
        embed.set_footer(**embed_default["footer"])
        await ctx.send(embed=embed)
      except:
        embed = discord.Embed(
          description=f"there was a problem while trying to change {user.name}'s nickname. make sure that the proper permissions are set for me!", color=0xffffff,
        )
        embed.set_footer(**embed_default["footer"])
        await ctx.send(embed=embed)
    else:
      embed = discord.Embed(
        description="access denied. ❌", color=0xffffff,
      )
      embed.set_footer(**embed_default["footer"])
      await ctx.send(embed=embed)

  @cog_ext.cog_slash(
    name="kick",
    description="kick a user from the server (requires 'kick members' permissions.)",
    options=[
      create_option(
        name="user",
        description="a discord user.",
        option_type=6,
        required=True
      ),
      create_option(
        name="reason",
        description="the kick reason to audit (defaults to none.)",
        option_type=3,
        required=False
      ),
    ],
    **command_default
  )
  async def _kick(self, ctx: SlashContext, user, reason="not specified."):
    if ctx.author.guild_permissions >= user.guild_permissions and ctx.author.guild_permissions.kick_members:
      try:
        await user.kick(reason=f"{reason} - {ctx.author}")
        embed = discord.Embed(
          description=f"successfully kicked {user.name}!", color=0xffffff,
        )
        embed.add_field(name="reason", value=str(reason), inline=False)
        embed.set_footer(**embed_default["footer"])
        await ctx.send(embed=embed)
      except:
        embed = discord.Embed(
          description=f"there was a problem while trying to kick {user.name}. make sure that the proper permissions are set for me!", color=0xffffff,
        )
        embed.set_footer(**embed_default["footer"])
        await ctx.send(embed=embed)
    else:
      embed = discord.Embed(
        description="access denied. ❌", color=0xffffff,
      )
      embed.set_footer(**embed_default["footer"])
      await ctx.send(embed=embed)

  @cog_ext.cog_slash(
    name="ban",
    description="ban a user from the server (requires 'ban members' permissions.)",
    options=[
      create_option(
        name="user",
        description="a discord user.",
        option_type=6,
        required=True
      ),
      create_option(
        name="reason",
        description="the ban reason to audit (defaults to none.)",
        option_type=3,
        required=False
      ),
    ],
    **command_default
  )
  async def _ban(self, ctx: SlashContext, user, reason="not specified."):
    if ctx.author.guild_permissions >= user.guild_permissions and ctx.author.guild_permissions.ban_members:
      try:
        await user.ban(reason=f"{reason} - {ctx.author}")
        embed = discord.Embed(
          description=f"successfully banned {user.name}!", color=0xffffff,
        )
        embed.add_field(name="reason", value=str(reason), inline=False)
        embed.set_footer(**embed_default["footer"])
        await ctx.send(embed=embed)
      except:
        embed = discord.Embed(
          description=f"there was a problem while trying to ban {user.name}. make sure that the proper permissions are set for me!", color=0xffffff,
        )
        embed.set_footer(**embed_default["footer"])
        await ctx.send(embed=embed)
    else:
      embed = discord.Embed(
        description="access denied. ❌", color=0xffffff,
      )
      embed.set_footer(**embed_default["footer"])
      await ctx.send(embed=embed)

  @cog_ext.cog_slash(
    name="purge",
    description="purge a specified amount of messages in a text channel (requires 'manage messages' permissions.)",
    options=[
      create_option(
        name="number",
        description="the number of messages to purge.",
        option_type=4,
        required=True
      )
    ],
    **command_default
  )
  async def _purge(self, ctx: SlashContext, number):
    if ctx.author.guild_permissions.manage_messages:
      try:
        messages_purged = await ctx.channel.purge(limit=int(number))
        embed = discord.Embed(
          description=f"successfully deleted {len(messages_purged)} messages!", color=0xffffff,
        )
        embed.set_footer(**embed_default["footer"])
        sent_message = await ctx.send(embed=embed)
        await asyncio.sleep(10)
        await sent_message.delete()
      except:
        pass
    else:
      embed = discord.Embed(
        description="access denied. ❌", color=0xffffff,
      )
      embed.set_footer(**embed_default["footer"])
      await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Moderation(bot))