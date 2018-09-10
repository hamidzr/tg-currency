import pickle
import re
from yaml import load, dump
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


def load(name):
  with open(name, 'rb') as f:
    return pickle.load(f)

def isPriceReport(msg):
  hasDollar = re.compile('#دلار')
  if (type(msg['message']) != str): return False
  if (msg['fwd']): return False
  if (hasDollar.search(msg['message']) == None): return False
  return True


def isInRange(num, aMin, aMax):
  return (num > aMin and num < aMax)

def parsePrice(num):
  # remove ,
  num = num.replace(',', '')
  return int(num)

def findDollarPrice(msg):
  text = msg['message']
  findNumbers = re.compile('[\d,]{4,8}')

  # zoom around dollar
  THRESH = 20
  # TODO find and get all the dollar prices not just the first one
  pos = re.search('#دلار', text).span()
  section = text[pos[0]-THRESH : pos[1]+THRESH]
  numbers = findNumbers.findall(section)

  if (not len(numbers)):
    print(section)
    return None

  numbers = map(parsePrice, numbers)
  numbers = list(filter(lambda n : isInRange(n, 2000, 30000), numbers))

  if (len(numbers) != 1):
    print(section)
    return None

  return (msg['date'], numbers[0])


def plotTimeseries(history):
  x = []
  y = []
  # history = history[0:2]
  history = list(filter(lambda x : x, history))
  for pt in history:
    x.append(pt[0])
    y.append(pt[1])
  print(x)
  print(y)
  plt.plot(x,y)
  plt.savefig('histogram.png')



# load the data
msgs = load('./dollarp-hist.pickle')
print(len(msgs), 'messages loaded')


# filter to find price reports
priceReports = list(filter(isPriceReport, msgs))
print(len(priceReports), 'price reports')

#inspect
# print(list(map(lambda m: str(m['date'].date()), msgs)))
history = list(map(findDollarPrice, priceReports))
# print(msgs[-10:])
plotTimeseries(history)

