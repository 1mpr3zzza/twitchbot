import os
import random
import json
from twitchio.ext import commands

# Загружаем статичные команды из файла
def load_commands():
    try:
        with open("commands.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

custom_commands = load_commands()

bot = commands.Bot(
    token=os.getenv('TOKEN'),
    prefix='!',
    initial_channels=[os.getenv('CHANNEL')]
)

chat_users = set()

@bot.event
async def event_ready():
    print(f'Бот подключен как {bot.nick}')

@bot.event
async def event_message(message):
    if message.echo:
        return

    chat_users.add(message.author.name)

    msg = message.content.strip()
    if msg.startswith("!"):
        cmd = msg[1:].split()[0]
        if cmd in custom_commands:
            await message.channel.send(custom_commands[cmd])

    await bot.handle_commands(message)

@bot.command(name='сосал')
async def сосал(ctx):
    candidates = list(chat_users - {ctx.author.name})
    if not candidates:
        await ctx.send(f"{ctx.author.name} сосал сам себя 😔")
    else:
        victim = random.choice(candidates)
        await ctx.send(f"{ctx.author.name} сосал {victim}")

bot.run()
