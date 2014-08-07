import time
import Cryptsy
#time to hold in cache, in seconds - this only applies for google AppEngine
ttc = 5

lastFetchTime = 0

cryptsy_pubkey = '45a04147f44cc0d2be0fadb60cf21255c067f87d'
cryptsy_privkey = '61f0e4bd5eaf6848fcbfb6fc077a4aeedebbc8fca3ac8851df73fe289b0d7481f2c731120bddbfd6'
def fetchMarketData():
    global lastFetchTime
    global cryptsy_pubkey
    global cryptsy_privkey
    global cryptsyHandle
    global marketData

    if getCachedTime():
        cryptsyHandle = Cryptsy.Cryptsy(cryptsy_pubkey, cryptsy_privkey)
        marketData = cryptsyHandle.getMarketDataV2()
        try:
            if marketData['success'] == 1:
                lastFetchTime = time.time()
        except:
            #fetchMarketData()
            raise("I do not know what to tell you man...")
def getLTCPrice():
    global cryptsyHandle
    cryptsyHandle = Cryptsy.Cryptsy(cryptsy_pubkey, cryptsy_privkey)
    r = cryptsyHandle.getSingleMarketData(3)
    try:
        return r['return']['markets']['LTC']['sellorders'][0]['price']
    except:
        getLTCPrice()

def getBalances():
    global cryptsyHandle
    cryptsyHandle = Cryptsy.Cryptsy(cryptsy_pubkey, cryptsy_privkey)
    r = cryptsyHandle.getInfo()
    return r['return']['balances_available']

def placeOrder(marketid, ordertype, quantity, price):
    global cryptsyHandle
    cryptsyHandle = Cryptsy.Cryptsy(cryptsy_pubkey, cryptsy_privkey)
    return cryptsyHandle.createOrder(marketid, ordertype, quantity, price)

def getCachedTime():
    return (time.time() - lastFetchTime) > ttc

def cancelOrder(orderid):
    return cryptsyHandle.cancelOrder(orderid)
