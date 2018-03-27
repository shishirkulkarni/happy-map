#!/usr/bin/env python

from TwitterAPI import TwitterAPI, TwitterRequestError
from config import *
import time
import os, sys
import pprint as pp


if len(sys.argv) == 1:
	print('Collector: Usage: collector.py "<search query>"');
	sys.exit(1)

api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, CONSUMER_ACCESS_TOKEN_KEY, CONSUMER_ACCESS_TOKEN_SECRET)

data_dir = os.path.join(DATA_BASEDIR, sys.argv[1])

if not os.path.exists(data_dir):
	try:
		os.mkdir(os.path.join(DATA_BASEDIR, sys.argv[1]))
	except:
		print('cannot create data dir')
		sys.exit(0)

query = " ".join([sys.argv[1], DEFAULT_QUERY_OPTIONS])

query_hash = {'q': query,
		"locale": "en",
		"tweet_mode": "extended",
		"count": 100}




# r = api.request("search/tweets", query_hash)

# pp.pprint(r.headers)

# for tweet in r:
# 	print(tweet['id'])

# sys.exit(0)


with open('Locations/geolocations.tsv') as locations:
	locations.readline()

	for line in locations:

		if line[0] == '#':
			continue

		if 'max_id' in query_hash:
			del query_hash['max_id']
		
		fields = line.strip().split("\t")

		file_path = os.path.join(data_dir, fields[0])
		mode = "a+" if os.path.exists(file_path) else "w+"
		print('getting data for ' + fields[0])
		geocode = ",".join([str(fields[1]), str(fields[2]), DEFAULT_SEARCH_RADIUS])
		query_hash['geocode'] = geocode

		with open(file_path, mode, encoding='utf-8') as datafile:
			while True:
				try:
					#time.sleep(6) # wait for 6 seconds so that rate limit doesnt exhaust
					r = api.request('search/tweets', query_hash)

					remaining_requests = int(r.headers['x-rate-limit-remaining'])
					remaining_time = int(r.headers['x-rate-limit-reset'])

					# print(remaining_requests)

					if remaining_requests == 1:
						print('sleeping for: ' + str((remaining_time - int(time.time()) + 10) / 60))
						time.sleep(remaining_time - int(time.time()) + 10)
						print('woke up!!!')
						break;


					tweet_ids = [item['id'] for item in r]

					if len(tweet_ids) == 0:
						print('got empty results')
						break;

					query_hash['max_id'] = min([item['id'] for item in r])
					

					for tweet in r:
						if tweet['id'] != query_hash['max_id']:
							datafile.write(tweet['full_text'] + '\n')
				
				except TwitterRequestError as e:
					print('An error occured')
					break

