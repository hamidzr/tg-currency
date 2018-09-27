import pickle
import re
from yaml import load, dump
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
figure(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')



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
    # print(section)
    return None

  numbers = map(parsePrice, numbers)
  numbers = list(filter(lambda n : isInRange(n, 2000, 30000), numbers))

  if (len(numbers) != 1):
    # print(section)
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
  # print(x)
  # print(y)
  plt.plot(x,y)
  plt.savefig('histogram.png')


# removes outliers from a sorted list based on a moving average
# returns indices of remained elements
def normalizeMovingAvg(numbers, windowSize=5, threshold=0.2):
  cleanIndices = []
  movingAvg = numbers[0]; # TODO better initialization for the moving average
  c = windowSize-1;
  while (c < len(numbers) - windowSize): # TODO check the boundaries
    sumDiff = numbers[c+1] - numbers[c-windowSize-1]
    movingAvg += sumDiff/windowSize
    if (numbers[c] < movingAvg + threshold * movingAvg and numbers[c] > movingAvg - threshold * movingAvg): # if in range
      cleanIndices.append(c)
    c += 1
  return cleanIndices


def normalize(hist):
  remainingHist = []
  prices = list(map(lambda x: x[1], hist))
  indices = normalizeMovingAvg(prices, windowSize=40, threshold=0.3)
  for i in indices:
    remainingHist.append(hist[i])
  return remainingHist


# load the data
msgs = load('./old-dollarp.pickle')
# print(len(msgs), 'messages loaded')


# filter to find price reports
priceReports = list(filter(isPriceReport, msgs))
# print(len(priceReports), 'price reports')

#inspect
# print(list(map(lambda m: str(m['date'].date()), msgs)))
history = list(filter(lambda x: x, map(findDollarPrice, priceReports)))
history = sorted(history, key=lambda x: x[0]) # sort it asc
print(f'history points before normalization: {len(history)}')
history = normalize(history)
print(f'history points after normalization: {len(history)}')
# print(history[:][1])
# print(list(map(lambda x: x[1], history)))

plotTimeseries(history)

