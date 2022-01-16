import discord
from discord.ext import commands
from discord.commands import Option
from discord.ext.commands import Cog

from Unban import database
from Unban.secrets import Website
from Unban.bot.ui import views
from typing import Union

class Moderation(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="ban", description="Ban a user.")
    async def ban(self, ctx: discord.ApplicationContext, user: Option(discord.Member, "The user to ban."), reason: Option(str, "The reason of the ban.", required=False, default="No reason provided.")):
        if   ctx.author.id == user.id: return await ctx.respond("You cannot ban yourself!", ephemeral=True)
        elif ctx.author.id == self.bot.user.id: return await ctx.respond("You cannot ban me via this command!", ephemeral=True)
        
        try:
            dialog = views.ConfirmDialog()
            await ctx.respond(f"Are you sure you want to ban {user}?", view=dialog)
            await dialog.wait()

            if dialog.value == True:
                await ctx.guild.ban(user, reason=reason)
                return await ctx.respond(f"User {user} has been banned for `{reason}`.", ephemeral=True)
            else: return await ctx.respond("The ban has been cancelled.", ephemeral=True)
        except Exception as e:
            if isinstance(e, discord.errors.ApplicationCommandInvokeError) or isinstance(e, discord.Forbidden):
                return await ctx.respond(f"User {user} could not be banned as I either do not have the correct permissions, or the user has a higher (or the same) position in the hierarchy!", ephemeral=True)
            else: return await ctx.respond(f"User {user} could not be banned because of an unknown error!", ephemeral=True)

    @commands.slash_command(name="unban", description="Unban a user.")
    async def unban(self, ctx: discord.ApplicationContext):
        return await ctx.respond(f"To unban someone, please go to my website: <{Website.HOST}>")
    
    @Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: Union[discord.User, discord.Member]):
        if isinstance(user, discord.User): return
        user: discord.Member

        try: return await user.send(f"You've been banned from `{guild.name}`! Please go to my website if you to make an unban request: <{Website.HOST}>.")
        except Exception: return
    
    @Cog.listener()
    async def on_message(self, message: discord.Message):
        msgs: database.Result = database.select(f"SELECT `messages` FROM `unban_bot`.`recent_messages` WHERE guildid = '{message.guild.id}' and userid = '{message.author.id}'")

        value = msgs.value

        if msgs.rows <= 0: return database.update(f"INSERT INTO `unban_bot`.`recent_messages` (`guildid`, `userid`, `messages`) VALUES ('{message.guild.id}', '{message.author.id}', '[\"{message.content}\"]')")
        elif len(value) >= 100: value.pop()
        value.insert(0, message.content)

        replaced = str(value).replace("'", "\"")

        return database.update(f"INSERT INTO `unban_bot`.`recent_messages` (`guildid`, `userid`, `messages`) VALUES ('{message.guild.id}', '{message.author.id}', '{replaced}')")

def setup(bot): bot.add_cog(Moderation(bot))