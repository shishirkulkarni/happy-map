#!/usr/bin/env python

from TwitterAPI import TwitterAPI

import pprint as pp

KEY = 'UGX4Yp0MT9sNEIYuQuL1kcLta'
SECRET = '3CcCa1Mg32ybJfzyWX81WR3uMvHwSkn8OwTauVOIbkJ7ZSg9Z1'

ACCESS_TOKEN = '830996731848486912-9hrNymJRdGM2dPr4Fe6oBZyoSdstxtH'
ACCESS_TOKEN_SECRET = '7pSce82yBnQe8BUTMES267lOSRhluZK0ew66OdMAcmpOW'

api = TwitterAPI(KEY, SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

r = api.request('search/tweets', {'q': "international women's day exclude:replies exclude:retweets", "locale": "en", "geocode": "40.7127753,-74.0059728,100mi", "tweet_mode": "extended", "count": 100})

for item in r:
	print(item['full_text'].strip())

