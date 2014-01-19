# -*- coding: utf-8 -*-

from Queue import Queue
from threading import Thread
from twython import TwythonStreamer
from twitterCredentials import *

from pyprocessing import *
import pprint

# LOCATIONS
world = "-180,-90,180,90"
europe = "-13,34,41,60"
usa = "-127,25,-64,50"
manhattan = "-74,40.7,-73.9,40.9"

loc = world
geoBounds = loc.split(",")

class StreamThread(Thread):
	""" Thread that initializes and runs Twython Stream """
	""" Modifies basic TwythonStreamer with addition of Queue """
	def __init__(self, stream_queue):
		Thread.__init__(self)
		self.stream_queue = stream_queue

	def run(self):
		self.stream = LiveStream(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, self.stream_queue)
		print "\nSTREAM INITIALIZED\n"

		
		self.stream.statuses.filter(locations=loc)
		
		# self.stream.statuses.sample()


class LiveStream(TwythonStreamer):
	""" Live stream from Twython """
	""" Modified from basic TwythonStreamer with addition of Queue """

	def __init__(self, APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, stream_queue):
		super(LiveStream, self).__init__(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
		self.stream_queue = stream_queue

	def on_success(self, data):
		# PUT COORDS IN QUEUE
		try:
			coordinates = data['coordinates']['coordinates']
			self.stream_queue.put(coordinates)
		except TypeError:
			pass
		except KeyError:
			pass

	def on_error(self, status_code, data):
		print('Error: {0}'.format(status_code))

stream_queue = Queue()
streaming = StreamThread(stream_queue)
streaming.start()

def setup():
	global scale_factor
	scale_factor = 2

	genWidth = int(abs(float(geoBounds[0]) - float(geoBounds[2])) * scale_factor)
	genHeight = int(abs(float(geoBounds[1]) - float(geoBounds[3])) * scale_factor)
	print genWidth, genHeight
	size(genWidth, genHeight, caption=loc)
	background(0)
	noStroke()

def draw():
	global stream_queue

	# DIM OLD DOTS
	fill(255, 0, 0, 5)
	rect(0, 0, width, height)
	
	# GET COORDS
	x = stream_queue.get()[0]
	y = stream_queue.get()[1]
	print x, y

	x = map(x, float(geoBounds[0]), float(geoBounds[2]), 0, width)
	y = height - map(y, float(geoBounds[1]), float(geoBounds[3]), 0, height)
	print x, y
	stream_queue.task_done()

	#CREATE BLUR/GLOW
	for i, v in enumerate(range(90, 0, -15)):
		fill(255, v)
		ellipse(x, y, i * 2 + 3, i * 2 + 3 )
	# CREATE DOT
	fill(255)
	ellipse(x, y, 4, 4)

run()
