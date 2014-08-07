#!/usr/bin/python
import fetcher
import operator
import sys
import time
import random
import smtplib
import urllib2
import json
import os
try:
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login("natebrune@gmail.com", "Wolfer3779")
except:
	pass
if len(sys.argv) == 2:
	ratio = float(sys.argv[1])
else:
	ratio = 0.99
if len(sys.argv) == 3:
	verb = sys.argv[2]
else:
	verb = 'n'

#.6% total fees (usually less)
fee_ratio = 0.008
def makemoney():
	simpleArb       = []
	ltcMarkets      = []
	btcMarkets      = []
	doubleMarkets   = []
	outBuff         = {}
	marketlookup    = {}
	#helper function to format floats
	def ff(f):
		return format(f, '.8f')

	try:
		print "\n\nFetching market data."

		fetcher.fetchMarketData()
		if verb == 'y':
			print "Processing market data."
		for market in fetcher.marketData['return']['markets']:
			mkid = fetcher.marketData['return']['markets'][market]['marketid']
			marketlookup[mkid] = market
		for marketName in fetcher.marketData['return']['markets']:
			try:
				lo_sell = fetcher.marketData['return']['markets'][marketName]['sellorders'][0]['price']
				hi_buy  = fetcher.marketData['return']['markets'][marketName]['buyorders'][0]['price']
				sn = fetcher.marketData['return']['markets'][marketName]['primarycode']
				marketid = fetcher.marketData['return']['markets'][marketName]['marketid']
				if hi_buy > lo_sell:
					proft = hi_buy - lo_sell
					simpleArb.append({'profit' : profit, 'market': marketName, 'hi_buy': hi_buy, 'lo_sell': lo_sell, 'sn': sn})
				if fetcher.marketData['return']['markets'][marketName]['secondarycode'] == 'LTC':
					ltcMarkets.append({'market': marketName, 'hi_buy': hi_buy, 'lo_sell': lo_sell, 'sn': sn, 'marketid': marketid})
				if fetcher.marketData['return']['markets'][marketName]['secondarycode'] == 'BTC':
					btcMarkets.append({'market': marketName, 'hi_buy': hi_buy, 'lo_sell': lo_sell, 'sn': sn, 'marketid': marketid})
			except:
				pass
	except:
		sys.exit("ERROR: Could not fetch market data.")



	try:
		if verb == 'y':
			print "Fetching LTC price."
		ltc_price = float(fetcher.getLTCPrice())
		if verb == 'y':
			print("LTC Price: " + format(ltc_price, '.8f')) 
	except:
		sys.exit("ERROR: Could not fetch LTC price.")

	try:
		if verb == 'y':
			print "Fetching balances."
		balances = fetcher.getBalances()
		btc_balance = float(balances['BTC']) - 0.000
		ltc_balance = float(balances['LTC'])
	except:
		sys.exit("ERROR: Could not fetch balances.")

	#check for simple arb opps
	for mkt in simpleArb:
		print(mkt['market'] + " : " + mkt['profit'])

	#check for ltc -> btc arb opps or btc -> ltc arb opps
	if verb == 'y':
		print "Processing arbitrage opportunities."
	for lmkt in ltcMarkets:
		for bmkt in btcMarkets:
			if lmkt['sn'] == bmkt['sn']:
				if verb == 'y':
					print("Checking " + lmkt['sn'] + "...")
				try:
					sn              = lmkt['sn']
					ltc_marketid    = lmkt['marketid']
					btc_marketid    = bmkt['marketid']
					ltc_hi_buy      = float(lmkt['hi_buy'])
					btc_hi_buy      = float(bmkt['hi_buy'])
					ltc_lo_sell     = float(lmkt['lo_sell'])
					btc_lo_sell     = float(bmkt['lo_sell'])
					ltc_hi_buy_btc  = ltc_hi_buy * ltc_price
					ltc_lo_sell_btc = ltc_lo_sell * ltc_price

					if verb == 'y':
						print("Comparing buy price of " + ff(ltc_lo_sell) + " LTC to sell price of " + ff(btc_hi_buy) + " BTC")
					if btc_hi_buy > ltc_lo_sell_btc:
						#profit to be made buying for LTC and selling for BTC
						num_purchasable = (ltc_balance / ltc_lo_sell) * ratio
						total_fees      = (num_purchasable * ltc_lo_sell) * fee_ratio
						total_profit    = ((btc_hi_buy - ltc_lo_sell) * num_purchasable) - total_fees
						if verb == 'y':
							print("Calculated total profit: " + ff(total_profit))
						outstr          = "buy " + ff(num_purchasable) + " " + sn
						outstr         += " @ " + ff(ltc_lo_sell) + " LTC"
						outstr         += " sell @ " + ff(btc_hi_buy) + " BTC"
						outstr         += " (" + ff(total_profit) + " BTC profit)? (y/n): "
						outBuff[total_profit] = {
							'outstr'            : outstr,
							'num_purchasable'   : num_purchasable,
							'buy_marketid'      : ltc_marketid,
							'sell_marketid'     : btc_marketid,
							'price'             : ff(ltc_lo_sell)
						}

					if verb == 'y':
						print("Comparing buy price of " + ff(btc_lo_sell) + " BTC to sell price of " + ff(ltc_hi_buy) + " LTC")
					if ltc_hi_buy_btc > btc_lo_sell:
						#profit to be made buying for BTC and selling for LTC
						num_purchasable = (btc_balance / btc_lo_sell) * ratio
						total_fees      = (num_purchasable * btc_lo_sell) * fee_ratio
						total_profit    = ((ltc_hi_buy_btc - btc_lo_sell) * num_purchasable) - total_fees
						if verb == 'y':
							print("Calculated total profit: " + ff(total_profit))
						outstr          = "buy " + ff(num_purchasable) + " " + sn
						outstr         += " @ " + ff(btc_lo_sell) + " BTC"
						outstr         += " sell @ " + ff(ltc_hi_buy) + " LTC"
						outstr         += " (" + ff(total_profit) + " BTC profit"
						outBuff[total_profit] = {
							'outstr'            : outstr,
							'num_purchasable'   : num_purchasable,
							'buy_marketid'      : btc_marketid,
							'sell_marketid'     : ltc_marketid,
							'price'             : ff(btc_lo_sell)
						}

					if verb == 'y':
						print("-----------")

				except:
					pass

	sorted_data = sorted(outBuff.iteritems(), key=operator.itemgetter(0), reverse=True)
	for (total_profit, data) in sorted_data:
		ret = ret = urllib2.urlopen(urllib2.Request('https://bitpay.com/api/rates'))
		a = ret.read()
		print(marketlookup[data['sell_marketid']].split('/')[0] + ':'+ " $"+ str(float(total_profit)*float(json.loads(a)[0]['rate']))[:8])
		if data['num_purchasable'] > 0 and total_profit > 0.0000001:
			r = fetcher.placeOrder(data['buy_marketid'], 'Buy', data['num_purchasable'], data['price'])
			print("Placed Buy order")
			if verb == 'y':
				print(r)
			lprice =fetcher.marketData['return']['markets'][marketlookup[data['sell_marketid']]]['buyorders'][0]['price']
			sucks = 0
			while True:
				balances = fetcher.getBalances()
				bbalance = float(balances[marketlookup[data['sell_marketid']].split('/')[0]])
				if(bbalance>0):
					break
				if(sucks>25):
					cancel = fetcher.cancelOrder(r['orderid'])
					break
				sucks = sucks+1
				#print "Balance of " + str(marketlookup[data['sell_marketid']].split('/')[0]) + " is still at "+str(bbalance)+", we didnt fill"
			if(sucks<25):
				balances = fetcher.getBalances()
				bbalance = float(balances[marketlookup[data['sell_marketid']].split('/')[0]])
				print("Im about to sell: "+str(bbalance) + marketlookup[data['sell_marketid']].split('/')[0])
				fetcher.placeOrder(data['sell_marketid'], 'Sell', bbalance, lprice)
				ret = ret = urllib2.urlopen(urllib2.Request('https://bitpay.com/api/rates'))
				a = ret.read()
				message = 'Subject: %s\n\n%s' % ("I just made: $"+ str(float(total_profit)*float(json.loads(a)[0]['rate'])), str(data['outstr']))
				try:
					server.sendmail("natebrune@gmail.com", "drewbrune@gmail.com", message)
				except:
					pass
				fetcher.cancelOrder(r['orderid'])
			else:
				print "We had to abort mission and cancel the order :^0"
		else:
			pass
makemoney()