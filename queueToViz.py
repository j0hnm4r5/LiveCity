from pyprocessing import *
import random
import threading
import Queue
import time

class Writer(threading.Thread):
	def __init__(self, queue):
		self.q = queue
		threading.Thread.__init__(self)

	def run(self):
		while True:
			self.q.put((random.randint(-180, 180), random.randint(-90, 90)))
			time.sleep(random.randint(10, 50) / 1000.0)


def setup():
	size(360, 180)
	background(0)
	noStroke()
	rectMode(CENTER)

	global q
	q = Queue.Queue()
	Writer(q).start()

def draw():
	global q
	translate(180, 90)

	# DIM OLD DOTS
	fill(0, 10)
	rect(0, 0, width, height)
	
	# GET COORDS
	x = q.get()[0]
	y = q.get()[1]
	q.task_done()

	#CREATE BLUR/GLOW
	for i, v in enumerate(range(90, 0, -15)):
		fill(255, v)
		ellipse(x, y, i * 2 + 3, i * 2 + 3 )
	# CREATE DOT
	fill(255)
	ellipse(x, y, 4, 4)

run()