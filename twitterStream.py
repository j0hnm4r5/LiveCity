from twython import TwythonStreamer
from twitterCredentials import *


class MyStreamer(TwythonStreamer):
	def on_success(self, data):
		if 'text' in data:
			print data['text'].encode('utf-8')
		

stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)



# stream.statuses.filter(track='berlin')
# stream.statuses.filter(locations='-74,40,-73,41')
stream.statuses.sample()