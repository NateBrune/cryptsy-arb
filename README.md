cryptsy-arb
===========

Python script for simple Cryptsy arbitrage

No special libraries or dependencies. Works best on Python 2.7.

Make sure to edit fetcher.py and put in your cryptsy public and private API keys.
Credit to https://github.com/dnase/cryptsy-arb for original script
Credit to https://github.com/ScriptProdigy/CryptsyPythonAPI for the Cryptsy API interface. I hacked it up a bit for my purposes.

Run with "python cmd.py [max % to spend in BTC/LTC as float] [Verbose (y)es or (n)o]"

i.e.

python cmd.py 0.25 n

or

chmod +x cmd.py
./cmd.py 0.33 n

Default max percentage to spend on a buy order is 99%.

This script will now make sell and buy orders!!

Advice: Resist the urge to convert LTC to BTC right after an arb oppertunity, you will loose $$$
There is not much money to be made on this exchange... perhaps because of this script closing the gaps

I am happy to receive your donations! 

BTC:
1MNiLXKDfQwMvKq1LD8xPttmufqnWtXvmW

I hope you use this script as reference on your way to becoming bitrich, good luck!

TO THE MOON!