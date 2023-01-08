# import dependencies
import os, discord, json, asyncio
from dotenv import load_dotenv
from discord.ext import commands
from discord_slash.utils.manage_commands import create_option
from discord_slash import SlashCommand
from discord_slash.error import DuplicateCommand
import globals
# import commands
from commands.basic import Basic
from commands.info import Info
from commands.moderation import Moderation
from commands.bot_owner import BotOwner
# import includes

# load secrets
load_dotenv()
# import settings
settings = None
with open("settings.json", "r") as settings_file:
    settings = json.load(settings_file)
# main bot init.
bot = commands.Bot(command_prefix=";", intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)
async def load_cogs(bot):
    bot.add_cog(Basic(bot))
    bot.add_cog(Info(bot))
    bot.add_cog(Moderation(bot))
    bot.add_cog(BotOwner(bot))

activity_object = None
class EveActivity:
    cached = discord.Activity(type=discord.ActivityType.playing, name="")
    def __main__(self):
        pass
    def set_cache(self, activity):
        self.cached = activity
    def get_cache(self):
        return self.cached

@bot.event
async def on_ready():
    print("ready! (:")
    globals.activity_object = EveActivity()
    activity = discord.Activity(type=discord.ActivityType.listening, name="cbat")
    globals.activity_object.set_cache(activity)
    await bot.change_presence(activity=activity)
    try:
        await load_cogs(bot)
    except DuplicateCommand:
        pass

# load in commands
bot.load_extension("commands.basic")
bot.load_extension("commands.info")
bot.load_extension("commands.moderation")
bot.load_extension("commands.bot_owner")
# start bot
#asyncio.new_event_loop()
#loop = asyncio.get_event_loop()

#loop.create_task(spotify_activity.check_activity(bot))

#loop.run_forever()

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(bot.start(os.getenv("TOKEN")))
    except KeyboardInterrupt:
        pass
