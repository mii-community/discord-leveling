from os import getenv

from dotenv import load_dotenv

load_dotenv()

# get token from .env
DISCORD_BOT_TOKEN = getenv("DISCORD_BOT_TOKEN")

# setting
BOT_NAME = "Mii Leveling System"
BOT_PREFIX = "!"

CH_LEVELUP_LOG = int(getenv("CH_NOTIFY", "806993148286861322"))
