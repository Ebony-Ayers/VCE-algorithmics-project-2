#/usr/bin/python
#Joseph Davies
from pynode.main import *
import ast
import sys

def on_click(node):
	print("Clicked on node \"{}\"".format(node.id()))

nodes = dict()
def get_node(name):
	if name in nodes:
		return nodes[name]
	else:
		node = graph.add_node(name)
		nodes[name] = node

def get_edge(node_1, node_2):
	if graph.adjacent(get_node(node_1), get_node(node_2)):
		return graph.edges_between(get_node(node_1), get_node(node_2))[0]
	else:
		edge = graph.add_edge(get_node(node_1), get_node(node_2))
		return edge

def run():	
	length_index = 2
	diameter_index = 3
	thickness_index = 7
	speed_index = 10
	
	if len(sys.argv) > 1:
		if sys.argv[1] != "-defaults":
			length_index = input("What collumn is the lengin in: ")
			diameter_index = input("What collumn is the diameter in: ")
			thickness_index = input("What collumn is the thicnkess in: ")
			speed_index = input("What collumn is the speed in: ")
	else:
		length_index = input("What collumn is the lengin in: ")
		diameter_index = input("What collumn is the diameter in: ")
		thickness_index = input("What collumn is the thicnkess in: ")
		speed_index = input("What collumn is the speed in: ")
	
	with open("pipes.csv", 'r') as csv_file:
		first = True
		for line in csv_file:
			#if it is the first line ignore it as it is the header
			if first:
				first = False
				continue
			#split the data into columns
			data = line.rstrip().lstrip().split(',')
			#where posible evaluate literals
			i = 0
			while i < len(data):
				try:
					data[i] = ast.literal_eval(data[i])
					i += 1
				except:
					i += 1
			
			
			for element in data:
				#get the edge between the two nodes in the line
				#if the edge does not exist create it
				#if either of the nodes do not exist create them
				e = get_edge(data[0], data[1])
				
				#set the values of the edge
				e.set_weight(data[length_index])
				e.set_attribute("length", data[length_index])
				e.set_attribute("inner radius", (data[diameter_index] - 2 * data[thickness_index]) / 2)
				e.set_attribute("speed", data[speed_index])
	
	register_click_listener(on_click)
begin_pynode(run)
