from pyprocessing import *
import couchdb


def setup():
	global db
	global live
	live = []
	size(800, 800)
	background(0)
	# rectMode(CENTER)
	noStroke()

	server = couchdb.Server()
	db = server['tweets-quick']

def draw():
	global db
	global live
	# background(0)

	fill(0,6)
	rect(0,0, width,height)

	for item in db:
		# print db[item]['coordinates']['coordinates']
		# boundingBox = 'long:-74,lat:40, long:-73,lat:41'

		longitude = (74 - -db[item]['coordinates']['coordinates'][0]) * 800
		latitude = (41 - db[item]['coordinates']['coordinates'][1]) * 800

		fill(255, 255, 255, 30)
		ellipse(int(longitude), int(latitude), 20, 20)

run()