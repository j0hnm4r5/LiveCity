import couchdb
from twython import TwythonStreamer
from twitterCredentials import *


class MyStreamer(TwythonStreamer):
	def on_success(self, data):
		print data['text'].encode('utf-8')

		tweet = data
		tweet['_id'] = tweet['id_str']
		db.save(tweet)
		

stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

server = couchdb.Server()
db = server['tweets-manhattan']

stream.statuses.filter(locations='-74,40,-73,41')
