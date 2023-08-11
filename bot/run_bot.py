"""Module for bot running."""
from services.bot import Bot

bot = Bot()
bot.create_users_and_tasks()
