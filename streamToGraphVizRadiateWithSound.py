from nodebox.graphics import *
from nodebox.graphics.physics import Node, Edge, Graph

from Queue import Queue
from threading import Thread

from twython import TwythonStreamer
from twitterCredentials import *

from time import clock, sleep
from math import sqrt

import liblo

try:
	# RUN: oscSetsNoteInChord.pd
	target = liblo.Address(44002)
except liblo.AddressError, err:
	print str(err)


""" LOCATIONS """
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

# SELECTED LOCATION GOES HERE
loc = northeast_usa

scale_factor = float(loc[1])
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

		self.stream.statuses.filter(locations=geoBounds)
		# self.stream.statuses.sample()

class LiveStream(TwythonStreamer):
	""" Live stream from Twython """
	""" Modified from basic TwythonStreamer with addition of Queue """

	def __init__(self, APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, stream_queue):
		super(LiveStream, self).__init__(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
		self.stream_queue = stream_queue

	def on_success(self, data):
		try:
			coordinates = data['coordinates']['coordinates']
			lon = coordinates[0]
			lat = coordinates[1]
			# place = data['place']['full_name'].encode('utf-8')
			# user = data['user']['screen_name'].encode('utf-8')
			# tweet = data['text'].encode('utf-8')
			bg_color = data['user']['profile_background_color']
			followers = data['user']['followers_count']
			self.stream_queue.put(((lon, lat), bg_color, followers))
		except (TypeError, KeyError, UnicodeDecodeError):
			# print "bad data"
			pass

	def on_error(self, status_code, data):
		print('Error: {0}'.format(status_code))

def distance(x1, y1, x2, y2):
	return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def convert_range(val, old_min, old_max, new_min, new_max):
	old_span = old_max - old_min
	new_span = new_max - new_min
	unitize = float(val - old_min) / float(old_span)
	return new_min + (unitize * new_span)

def add_node(x, y, node_color, followers_count):
	global n

	new = g.add_node(id=n, fill=None, stroke=node_color + [1], text=None, radius=20)
	new.x = x
	new.y = y

	scale_down_followers = 50

	if len(g.nodes) < int(followers_count / scale_down_followers):
		num_local = len(g.nodes) - 1
		num_global = num_local - int(followers_count / scale_down_followers)
	else:
		num_local = int(followers_count / scale_down_followers)
		num_global = 0

	for m in range(num_local):
		node = choice(g.nodes)
		if node != new:
			g.add_edge(new, node, stroke=color(.4), length=distance(new.x, new.y, node.x, node.y))

	for m in range(num_global):
		stroke(.5)
		strokestyle(style=DASHED)

		wall = random(0, 4)
		if wall == 0:
			line(-canvas.width / 2, random(-canvas.height / 2, canvas.height / 2), new.x, new.y)
		elif wall == 1:
			line(canvas.width / 2, random(-canvas.height / 2, canvas.height / 2), new.x, new.y)
		elif wall ==2:
			line(random(-canvas.width / 2, canvas.width / 2), -canvas.height / 2, new.x, new.y)
		else:
			line(random(-canvas.width / 2, canvas.width / 2), canvas.height / 2, new.x, new.y)

		strokestyle(style=SOLID)

	pick_notes_then_send(num_local + num_global)
	n += 1

def pick_notes_then_send(num_connections):
	chord = [1, 0, 0, 0, 0, 0, 0]
	# print num_connections

	if 5 <= num_connections:
		chord[1] = 1
	if 10 <= num_connections:
		chord[2] = 1
	if 15 <= num_connections:
		chord[3] = 1
	if 20 <= num_connections:
		chord[4] = 1
	if 25 <= num_connections:
		chord[5] = 1
	if 30 <= num_connections:
		chord[6] = 1

	# Connections to send: /bang, /fund, /h1, /h2, /h3, /h4, /h5, /h6, /x

	liblo.send(target, "/fund", chord[0])
	liblo.send(target, "/h1", chord[1])
	liblo.send(target, "/h2", chord[2])
	liblo.send(target, "/h3", chord[3])
	liblo.send(target, "/h4", chord[4])
	liblo.send(target, "/h5", chord[5])
	liblo.send(target, "/h6", chord[6])
	liblo.send(target, "/bang", 1)
	liblo.send(target, "/fund", 0)
	liblo.send(target, "/h1", 0)
	liblo.send(target, "/h2", 0)
	liblo.send(target, "/h3", 0)
	liblo.send(target, "/h4", 0)
	liblo.send(target, "/h5", 0)
	liblo.send(target, "/h6", 0)

	# print chord

def change_key(base_freq):
	# Connections to send: /f, /1/1, /1/2, /2/1, /2/2, /3/1, /3/2, /4/1, /4/2, /5/1, /5/2, /6/1, /6/2

	# m13 chord

	liblo.send(target, "/f", base_freq)

	liblo.send(target, '/1/1', 19)
	liblo.send(target, '/1/2', 16)

	liblo.send(target, '/2/1', 3)
	liblo.send(target, '/2/2', 2)

	liblo.send(target, '/3/1', 7)
	liblo.send(target, '/3/2', 4)

	liblo.send(target, '/4/1', 9 * 2)
	liblo.send(target, '/4/2', 8)

	liblo.send(target, '/5/1', 21 * 2)
	liblo.send(target, '/5/2', 16)

	liblo.send(target, '/6/1', 27 * 2)
	liblo.send(target, '/6/2', 16)


g = Graph()
n = 0


g.distance = 10
g.layout.force = 0
g.layout.repulsion = 10 # Repulsion radius

# change_key(261.63)
change_key(440)


def draw(canvas):
	global stream_queue
	# canvas.clear()
	background(1, .1)

	translate(canvas.width / 2, canvas.height / 2)

	g.draw()
	g.update()

	# GET DATA
	if stream_queue.qsize() > 0:
		data = stream_queue.get_nowait()
		stream_queue.task_done()

		lon = data[0][0]
		lat = data[0][1]
		x = convert_range(lon, float(geoBounds[0]), float(geoBounds[2]), -canvas.width / 2, canvas.width / 2)
		y = convert_range(lat, float(geoBounds[1]), float(geoBounds[3]), -canvas.height / 2, canvas.height / 2)

		node_color = [m / 255.0 for m in [ord(c) for c in data[1].decode('hex')]]

		followers_count = data[2]

		add_node(x, y, node_color, followers_count)

	now = clock()
	for node in g.nodes:
		node.radius *= 1.1
		if now - node.age > 8:
			g.remove(node)

stream_queue = Queue()
streaming = StreamThread(stream_queue)
streaming.start()

canvas = Canvas(name=loc[2], resizable=True)

canvas.width = (float(geoBounds[2]) - float(geoBounds[0])) * scale_factor
canvas.height = (float(geoBounds[3]) - float(geoBounds[1])) * scale_factor

# canvas.fullscreen = True
canvas.run(draw)
