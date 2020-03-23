#/usr/bin/python
#Joseph Davies
from pynode.main import *
import ast
import sys
import time

node_1 = None
node_2 = None
active_edge = None
node_clear = None

sensor_nodes = list()
break_nodes = list()

def reset():
	global node_1, node_2, active_edge
	if node_1 in sensor_nodes:
		node_1.set_color(Color(150, 50, 150))
	elif node_1 in break_nodes:
		node_1.set_color(Color(50, 100, 200))
	else:
		node_1.set_color(Color.DARK_GREY)
	if node_2 in sensor_nodes:
		node_2.set_color(Color(150, 50, 150))
	elif node_2 in break_nodes:
		node_2.set_color(Color(50, 100, 200))
	else:
		node_2.set_color(Color.DARK_GREY)
	if active_edge is not None:
		active_edge.set_color(Color.LIGHT_GREY)
	node_1 = None
	node_2 = None
	active_edge = None
	
def is_float(posible_int):
	output = False
	try:
		output = float(posible_int)
	except:
		output = False
	return output
	
def prompt(request_length = False):
	first = None
	second = None
	while True:
		print("What would you like to do:")
		input_1 = input("Add a break (b), add a sensor (s), cancel (c): ").lower().rstrip()
		if input_1 == "b":
			first = input_1
			break
		elif input_1 == "s":
			first = input_1
			break
		elif input_1 == "c":
			return (None, None)
		else:
			print("Invalid Input")
	
	if request_length:
		while True:
			input_2 = is_float(input("How far along the pipe do you want to add it in meters: ").lower().rstrip())
			if input_2 != False:
				second = input_2
				break
			else:
				print("Invalid Input")
		
	return (first, second)

def on_click(node):
	global node_1, node_2, active_edge
	print("Clicked on node \"{}\"".format(node.id()))
	
	if node is node_clear:
		reset()
		
	if node_1 is not None and node_2 is not None:
		reset()
	
	if node_1 is None:
		node_1 = node
		node_1.set_color(Color.YELLOW)
	elif node_2 is None:
		node_2 = node
		node_2.set_color(Color.GREEN)
		
	if node_1 is not None and node_2 is not None and node_1 is not node_2:
		try:
			active_edge = graph.edges_between(node_1, node_2)[0]
			active_edge.set_color(Color.BLUE)
			print("start")
			active_edge.traverse(initial_node=active_edge.source(), color=Color.RED, keep_path=True, length=10000.0)
			
		except Exception as e:
			print("Cannot find edge between selected nodes")
			print(e)
			return
			
	if node_1 is not None and node_2 is not None:
		if active_edge is not None:
			new_thing_type, new_thing_length = prompt(True)
		else:
			new_thing_type, new_thing_length = prompt(False)
		
		if new_thing_type is None and new_thing_length is None:
			reset()
			return
		
		if new_thing_length != None:
			if new_thing_type == "b":
				new_node = graph.add_node("Break: " + str(len(break_nodes) + 1))
				new_node.set_color(Color(50, 100, 200))
				length_1 = round(new_thing_length, 1)
				length_2 = round(active_edge.weight() - new_thing_length, 1)
				new_edge_1 = graph.add_edge(node_1, new_node)
				new_edge_1.set_weight(length_1)
				new_edge_2 = graph.add_edge(new_node, node_2)
				new_edge_2.set_weight(length_2)
				graph.remove_edge(active_edge)
				active_edge = None
				break_nodes.append(new_node)
			elif new_thing_type == "s":
				new_node = graph.add_node("Sensor: " + str(len(sensor_nodes) + 1))
				new_node.set_color(Color(150, 50, 150))
				length_1 = round(new_thing_length, 1)
				length_2 = round(active_edge.weight() - new_thing_length, 1)
				new_edge_1 = graph.add_edge(node_1, new_node)
				new_edge_1.set_weight(length_1)
				new_edge_2 = graph.add_edge(new_node, node_2)
				new_edge_2.set_weight(length_2)
				graph.remove_edge(active_edge)
				active_edge = None
				sensor_nodes.append(new_node)
		else:
			if new_thing_type == "b":
				things_to_reconect_to = list()
				for edge in node_1.incident_edges():
					things_to_reconect_to.append((edge.other_node(node_1), edge.weight()))
				graph.remove_node(node_1)
				new_node = graph.add_node("Break: " + str(len(break_nodes) + 1))
				new_node.set_color(Color(50, 100, 200))
				for thing in things_to_reconect_to:
					node_to_conect_to, weight = thing
					new_edge = graph.add_edge(new_node, node_to_conect_to)
					new_edge.set_weight(weight)
				break_nodes.append(new_node)
			elif new_thing_type == "s":
				things_to_reconect_to = list()
				for edge in node_1.incident_edges():
					things_to_reconect_to.append((edge.other_node(node_1), edge.weight()))
				graph.remove_node(node_1)
				new_node = graph.add_node("Sensor: " + str(len(sensor_nodes) + 1))
				new_node.set_color(Color(150, 50, 150))
				for thing in things_to_reconect_to:
					node_to_conect_to, weight = thing
					new_edge = graph.add_edge(new_node, node_to_conect_to)
					new_edge.set_weight(weight)
				sensor_nodes.append(new_node)
		
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
	global node_clear
	
	node_clear = graph.add_node("Clear")
	node_clear.set_color(Color.RED)
	node_clear.set_position(50, 480)
	
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
