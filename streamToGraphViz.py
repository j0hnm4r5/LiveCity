from nodebox.graphics import *
from nodebox.graphics.physics import Node, Edge, Graph

from Queue import Queue
from threading import Thread

from twython import TwythonStreamer
from twitterCredentials import *

from time import clock, sleep
from math import sqrt


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
loc = new_york

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
			self.stream_queue.put_nowait((lon, lat))
		except (TypeError, KeyError, UnicodeDecodeError):
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

def add_node(x, y):
	global n
	new = g.add_node(id=n, fill=color(1, .25), stroke=None, text=None)
	new.x = x
	new.y = y

	closest_list = []
	if len(g.nodes) > 1:
		for node in g.nodes:
			if distance(node.x, node.y, new.x, new.y) < canvas.width / 8:
				closest_list.append(node)
		for node in closest_list:
			g.add_edge(new, node, stroke=color(1), length=distance(new.x, new.y, node.x, node.y))
	n += 1
	# print "Node added at %d, %d" % (x, y)

g = Graph()
n = 0

g.distance = 10
g.layout.force = 0
g.layout.repulsion = 10 # Repulsion radius

def draw(canvas):
	global stream_queue
	canvas.clear()
	background(0)

	translate(canvas.width / 2, canvas.height / 2)

	g.draw()
	g.update()

	# GET DATA
	if stream_queue.qsize() > 0:
		data = stream_queue.get_nowait()
		stream_queue.task_done()

		lon = data[0]
		lat = data[1]
		# print lon, lat
		x = convert_range(lon, float(geoBounds[0]), float(geoBounds[2]), -canvas.width / 2, canvas.width / 2)
		y = convert_range(lat, float(geoBounds[1]), float(geoBounds[3]), -canvas.height / 2, canvas.height / 2)
		# print x, y
		add_node(x, y)

	now = clock()
	for node in g.nodes:
		node.radius = ((now - node.age) * 5)
		if now - node.age > 10:
			g.remove(node)

stream_queue = Queue()
streaming = StreamThread(stream_queue)
streaming.start()

canvas.width = (float(geoBounds[2]) - float(geoBounds[0])) * scale_factor
canvas.height = (float(geoBounds[3]) - float(geoBounds[1])) * scale_factor
canvas.run(draw)
