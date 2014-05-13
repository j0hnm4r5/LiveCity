from nodebox.graphics import *
from nodebox.graphics.physics import Node, Edge, Graph

from time import clock, sleep
from math import sqrt

from random import uniform

import liblo

try:
	target = liblo.Address(44001)
except liblo.AddressError, err:
	print str(err)

def convert_range(val, old_min, old_max, new_min, new_max):
	old_span = old_max - old_min
	new_span = new_max - new_min
	unitize = float(val - old_min) / float(old_span)
	return new_min + (unitize * new_span)

def distance(x1, y1, x2, y2):
	return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def add_node(x, y):
	global n
	new = g.add_node(id=n, fill=color(0), stroke=None, text=None, radius=5)
	new.x = x
	new.y = y

	closest_list = []
	if len(g.nodes) > 1:
		for node in g.nodes:
			if distance(node.x, node.y, new.x, new.y) < canvas.width / 8:
				closest_list.append(node)
		for node in closest_list:
			# g.add_edge(new, node, stroke=color(0), length=convert_range(x + canvas.width / 2, 0, canvas.width, .01, 20))
			edge = g.add_edge(new, node, length=(new.x + canvas.width / 2 + 1))

	n += 1
	# pick_notes_then_send(len(closest_list))

def pick_notes_then_send(n):
	chord = [1, 0, 0, 0]

	if n > 0:
		chord[1] = 1
	if n > 1:
		chord[2] = 1
	if n > 2:
		chord[2] = 1

	liblo.send(target, "/fund", chord[0])
	liblo.send(target, "/h1", chord[1])
	liblo.send(target, "/h2", chord[2])
	liblo.send(target, "/h3", chord[3])
	liblo.send(target, "/bang", 1)
	liblo.send(target, "/fund", 0)
	liblo.send(target, "/h1", 0)
	liblo.send(target, "/h2", 0)
	liblo.send(target, "/h3", 0)

g = Graph()
n = 0

g.distance = 30
g.layout.force = 1
g.layout.repulsion = 1 # Repulsion radius

def draw(canvas):
	canvas.clear()
	background(1)

	translate(canvas.width / 2, canvas.height / 2)

	g.draw()
	g.update()
	
	# Undo translate()
	dx = canvas.mouse.x - canvas.width / 2 
	dy = canvas.mouse.y - canvas.height / 2

	if canvas.mouse.pressed:
		add_node(dx, dy)

	now = clock()
	for node in g.nodes:
		if now - node.age > 5:
			g.remove(node)


canvas = Canvas(width=1920 / 3, height=1080 / 3, name="Draw Graph", resizable=True)
# canvas.fullscreen = True
canvas.run(draw)
