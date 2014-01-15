from twython import TwythonStreamer
# from twython import Twython
from twitterCredentials import *

import pprint


class MyStreamer(TwythonStreamer):
	def on_success(self, data):
		# pprint.pprint(data)
		print "****************************************"
		# if 'text' in data:
		print data['coordinates']
		

stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
# twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)



# stream.statuses.filter(track='berlin')
stream.statuses.filter(locations='-74,40,-73,41')
# stream.statuses.sample()

