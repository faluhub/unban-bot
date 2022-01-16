from Unban import secrets, database
from Unban.website import app
from Unban.bot import bot

if __name__ == "__main__":
    database._create_tables()

    bot.start(secrets.Bot.TOKEN)