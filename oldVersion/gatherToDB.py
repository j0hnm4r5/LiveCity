import couchdb
from twython import TwythonStreamer
from twitterCredentials import *


class MyStreamer(TwythonStreamer):
	def on_success(self, data):
		print data['text'].encode('utf-8')
		if data['coordinates'] != None:
			print data['coordinates']
			tweet = data
			tweet['_id'] = tweet['id_str']
			db.save(tweet)
		

stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

server = couchdb.Server()
db = server['tweets-quick']

stream.statuses.filter(locations='-74,40,-73,41')
# stream.statuses.filter(locations='-74.023908,40.766972,-73,41')
