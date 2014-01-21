# -*- coding: utf-8 -*-

from Queue import Queue
from threading import Thread
from twython import TwythonStreamer
from twitterCredentials import *
from pyprocessing import *
from datetime import datetime
import sys

import pprint

# LOCATIONS
# format: ("W,S,E,N", scale_factor, title, file_name)
world = ("-180,-90,180,90", 3, "Earth")
europe = ("-13,34,41,60", 15, "Europe")
germany = ("5.3,47.2,15.6,55", 75, "Germany")
uk = ("-10.9,49.7,2.4,59.4", 75, "British Isles")
usa = ("-127,25,-64,50", 20, "USA")
manhattan = ("-74.02,40.7,-73.89,40.9", 3000, "Manhattan, NYC")
nyc = ("-74,40,-73,41", 750, "New York City")
boston = ("-71.3,42.2,-70.9,42.5", 2000, "Boston, MA")
northeast_usa = ("-80.6,38.2,-66.4,47.6", 75, "Northeastern USA")
new_york = ("-80,40.2,-71.3,46", 100, "New York State")
carribean = ("-63.58,11.58,-58.79,18.66", 100, "Lower Antilles")

# LOCATION GOES HERE
# loc = sys.argv[1]
loc = world

scale_factor = loc[1]
geoBounds = loc[0]
geoBounds = geoBounds.split(",")

class StreamThread(Thread):
	""" Thread that initializes and runs Twython Stream """
	""" Modifies basic TwythonStreamer with addition of Queue """
	def __init__(self, stream_queue):
		Thread.__init__(self)
		self.stream_queue = stream_queue

	def run(self):
		self.stream = LiveStream(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, self.stream_queue)
		print "STREAM INITIALIZED"		
		
		self.stream.statuses.filter(locations=loc[0])
		# self.stream.statuses.sample()

class LiveStream(TwythonStreamer):
	""" Live stream from Twython """
	""" Modified from basic TwythonStreamer with addition of Queue """

	def __init__(self, APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, stream_queue):
		super(LiveStream, self).__init__(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
		self.stream_queue = stream_queue

	def on_success(self, data):
		# PUT JSON IN QUEUE
		self.stream_queue.put(data)

	def on_error(self, status_code, data):
		print('Error: {0}'.format(status_code))

stream_queue = Queue()
streaming = StreamThread(stream_queue)
streaming.start()

def setup():
	genWidth = int(abs(float(geoBounds[0]) - float(geoBounds[2])) * scale_factor)
	genHeight = int(abs(float(geoBounds[1]) - float(geoBounds[3])) * scale_factor)
	# print "Window Size: %s x %s\n" % (genWidth, genHeight)
	size(genWidth, genHeight, caption=loc[2] + ", Starting at: " + str(datetime.now()))
	background(0)
	noStroke()

	try:
		im = loadImage('/Users/johnmars/Development/LiveCity/Images/' + loc[3])
		scale(float(genHeight) / float(im.height))
		image(im, 0, 0)
	except IndexError:
		pass

def draw():
	global stream_queue

	# DIM OLD DOTS
	fill(0, 5)
	rect(0, 0, width, height)
	
	# GET DATA
	data = stream_queue.get()
	stream_queue.task_done()

	try:
		coordinates = data['coordinates']['coordinates']
		lon = coordinates[0]
		lat = coordinates[1]
		# place = data['place']['full_name'].encode('utf-8')
		# user = data['user']['screen_name'].encode('utf-8')
		# tweet = data['text'].encode('utf-8')
		# print coordinates, place, user, tweet
		print lon, lat
		x = map(lon, float(geoBounds[0]), float(geoBounds[2]), 0, width)
		y = height - map(lat, float(geoBounds[1]), float(geoBounds[3]), 0, height)
		
		#CREATE BLUR/GLOW
		for i, v in enumerate(range(90, 0, -15)):
			fill(255, v)
			ellipse(x, y, i * 2 + 3, i * 2 + 3 )

		# CREATE DOT
		fill(255)
		ellipse(x, y, 4, 4)
		# textSize(8)
		# text(place, x, y)
	except (TypeError, KeyError, UnicodeDecodeError):
		pass	


run()
