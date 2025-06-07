from twitchio.ext import commands
import json

# Загружаем кастомные команды из файла
def load_commands():
    try:
        with open("commands.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

custom_commands = load_commands()

bot = commands.Bot(
    token='oauth:ТВОЙ_ТОКЕН',
    prefix='!',
    initial_channels=['ТВОЙ_КАНАЛ']
)

@bot.event
async def event_ready():
    print(f'Бот запущен как | {bot.nick}')

@bot.event
async def event_message(message):
    if message.echo:
        return

    msg = message.content.strip()
    if msg.startswith("!"):
        cmd = msg[1:].split()[0]
        if cmd in custom_commands:
            await message.channel.send(custom_commands[cmd])

    await bot.handle_commands(message)

bot.run()
