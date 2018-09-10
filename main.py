from telethon import TelegramClient, sync
from datetime import datetime
import pickle
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# get your own api_id and api_hash from https://my.telegram.org, under API Development.
API_ID = config['DEFAULT']['TG_API_ID']
API_HASH = config['DEFAULT']['TG_API_HASH']
USERNAME = 'dollarp'


def save(data, name='save'):
  with open(f'{name}.pickle', 'wb') as f:
    pickle.dump(data, f)

def filterObject(dic, attrs):
  res = {}
  for att in attrs:
    try:
      res[att] = getattr(dic, att)
    except Exception as e:
      pass
  return res

def clean(msg):
  impAttrs = ['message', 'id', 'date', 'from_id']
  newObj = filterObject(msg, impAttrs)
  newObj['IsFwd'] = True if (msg.fwd_from) else False
  return newObj

client = TelegramClient('session_name', API_ID, API_HASH)
client.start()
me = client.get_me()

msgs = client.get_messages(USERNAME, limit=None)

# inspect
# print(msgs[6])
# ats = list(map(lambda m : m.post, msgs))
# print(ats)

# trim
nMsgs = map(clean, msgs)

save(list(nMsgs), f'{USERNAME}-hist')
