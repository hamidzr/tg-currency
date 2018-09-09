from telethon import TelegramClient, sync
import pickle
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# get your own api_id and api_hash from https://my.telegram.org, under API Development.
API_ID = config['DEFAULT']['TG_API_ID']
API_HASH = config['DEFAULT']['TG_API_HASH']

client = TelegramClient('session_name', API_ID, API_HASH)
client.start()

print(client.get_me().stringify())

messages = client.get_messages('dollarp', limit=10)
