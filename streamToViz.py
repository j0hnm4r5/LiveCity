# -*- coding: utf-8 -*-

from Queue import Queue
from threading import Thread
from twython import TwythonStreamer
from twitterCredentials import *

from pyprocessing import *



class StreamThread(Thread):
	""" Thread that initializes and runs Twython Stream """
	""" Modifies basic TwythonStreamer with addition of Queue """
	def __init__(self, stream_queue):
		Thread.__init__(self)
		self.stream_queue = stream_queue

	def run(self):
		self.stream = LiveStream(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, self.stream_queue)
		print "STREAM INITIALIZED"
		self.stream.statuses.filter(locations="-180,-90,180,90")
		# self.stream.statuses.sample()


class LiveStream(TwythonStreamer):
	""" Live stream from Twython """
	""" Modified from basic TwythonStreamer with addition of Queue """

	def __init__(self, APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, stream_queue):
		super(LiveStream, self).__init__(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
		self.stream_queue = stream_queue

	def on_success(self, data):
		# PUT COORDS IN QUEUE
		if 'coordinates' in data:
			if data['coordinates'] != None:
				coordinates = data['coordinates']['coordinates']
				place = None
				if 'place' in data:
					if data['place'] != None:
						if 'name' in data['place']:
							if data['place']['name'] != None:
								place = data['place']['name']
				self.stream_queue.put((coordinates, place))

	def on_error(self, status_code, data):
		print('Error: {0}'.format(status_code))

stream_queue = Queue()
streaming = StreamThread(stream_queue)
streaming.start()

def setup():
	global scale_factor
	scale_factor = 2
	size(360 * scale_factor, 180 * scale_factor)
	background(0)
	noStroke()
	rectMode(CENTER)

def draw():
	global stream_queue

	# ACCOUNT FOR NEGATIVE LAT/LONG
	translate(180 * scale_factor, 90 * scale_factor)

	# DIM OLD DOTS
	fill(0, 10)
	rect(0, 0, width, height)
	
	# GET COORDS
	x = stream_queue.get()[0][0] * scale_factor
	y = -stream_queue.get()[0][1] * scale_factor
	place = stream_queue.get()[1]
	stream_queue.task_done()
	print -y, x, place.encode('utf-8')

	#CREATE BLUR/GLOW
	for i, v in enumerate(range(90, 0, -15)):
		fill(255, v)
		ellipse(x, y, i * 2 + 3, i * 2 + 3 )
	# CREATE DOT
	fill(255)
	ellipse(x, y, 4, 4)

run()
