import os
from discord.ext.commands import AutoShardedBot
from discord.ext.commands.bot import T

if __name__ == "__main__": exit("You may not run the program from the bot file!") # prevents people from running the bot file

class UnbanBot(AutoShardedBot):
    def __init__(self):
        self.cog_blacklist        = [] # for testing purposes only
        self.cog_folder_blacklist = ["__pycache__"] # for testing purposes only (leave __pycache__ in here)

        super().__init__(
            command_prefix  ="$",
            case_insensitive=True,
            help_command    =None,
            description     ="An unban-request bot with a nice looking UI!",
            debug_guilds    =[915703368696082472]
        )
    
    def load_cogs(self, root=False):
        if root: print("Loading cogs...")

        for file in os.listdir("./Unban/bot/cogs"):
            if not file in self.cog_blacklist and not file in self.cog_folder_blacklist:
                try:
                    self.load_extension(f"Unban.bot.cogs.{file[:-3]}")
                    if root: print(f"  Loaded cog: {file}")
                except Exception as e: print(str(e))
            elif os.path.isdir(f"./cogs/{file}") and not file in self.cog_folder_blacklist:
                if root: print(f"  Loading cogs from {file}:")
                for subfile in os.listdir(f"./Unban/bot/cogs/{file}"):
                    if not subfile in self.cog_blacklist:
                        try:
                            self.load_extension(f"Unban.bot.cogs.{file}.{subfile[:-3]}")
                            if root: print(f"    Loaded cog: {subfile}")
                        except Exception as e: print(str(e))
    
    async def on_connect(self): return [print("Connected"), self.load_cogs(root=True), await self.register_commands()]
    async def on_ready(self):   return [print("Ready")]

def start(token): UnbanBot().run(token)
