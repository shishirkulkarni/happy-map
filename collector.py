#!/usr/bin/env python

from TwitterAPI import TwitterAPI
from config import *

api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, CONSUMER_ACCESS_TOKEN_KEY, CONSUMER_ACCESS_TOKEN_SECRET)

r = api.request('search/tweets', 
			{'q': "international women's day exclude:replies exclude:retweets",
			"locale": "en",
			"geocode": "40.7127753,-74.0059728,100mi",
			"tweet_mode": "extended",
			"count": 100})

for item in r:
	print(item['full_text'].strip())

