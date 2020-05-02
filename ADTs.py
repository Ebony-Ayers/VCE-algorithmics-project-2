#/usr/bin/python
#Joseph Davies 2020
#https://github.com/Joseph-Davies/vce-algroithmics-adts

class queue:
	def __init__(self):
		self._container = list()
		
	def enqueue(self, element):
		self._container.append(element)
	
	def dequeue(self):
		element = self._container[0]
		self._container.pop(0)
		return element
		
	def front(self):
		return self._container[0]
	
	def back(self):
		return self._container[-1]
	
	def at(self, index):
		return self._container[index]
	
	def length(self):
		return len(self._container)
	
	def __len__(self):
		return len(self._container)
	
	def __str__(self):
		output = "queue {"
		output += str(self._container[0])
		for element in self._container[1:]:
			output += ", " + str(element)
		output += "}"
		return output
	
	def __repr__(self):
		output = "queue {"
		output += str(self._container[0])
		for element in self._container[1:]:
			output += ", " + str(element)
		output += "}"
		return output
	
	def to_list(self):
		return self._container

class priority_queue:
	def __init__(self):
		self._container = list()
	
	def enqueue(self, element, priority):
		packet = (element, priority)
		
		if len(self._container) == 0:
			self._container.append(packet)
			return
		
		i = 0
		while i < len(self._container):
			if self._container[i][1] > priority:
				self._container.insert(i, packet)
				break
			i += 1
			
	def dequeue(self):
		element = self._container[0]
		self._container.pop(0)
		return element
	
	def front(self):
		return self._container[0]
	
	def back(self):
		return self._container[-1]
	
	def at(self, index):
		return self._container[index]
	
	def length(self):
		return len(self._container)
	
	def __len__(self):
		return len(self._container)
	
	def __str__(self):
		output = "priotiry queue {"
		output += str(self._container[0])
		for element in self._container[1:]:
			output += ", " + str(element)
		output += "}"
		return output
		
	def __repr__(self):
		output = "priotiry queue {"
		output += str(self._container[0])
		for element in self._container[1:]:
			output += ", " + str(element)
		output += "}"
		return output
	
	def to_list(self):
		return self._container

class stack:
	def __init__(self):
		self._container = list()
	
	def push(self, element):
		self._container.append(element)
	
	def pop(self):
		element = self._container[-1]
		self._container.pop()
		return element
	
	def top(self):
		return self._container[-1]
	
	def botom(self):
		return self._container[0]
	
	def at(self, index):
		return self._container[-1 * (index + 1)]
	
	def length(self):
		return len(self._container)
	
	def __len__(self):
		return len(self._container)
	
	def __str__(self):
		output = "stack {"
		output += str(self._container[-1])
		for element in self._container[1::-1]:
			output += ", " + str(element)
		output += "}"
		return output
		
	def __repr__(self):
		output = "stack {"
		output += str(self._container[-1])
		for element in self._container[1::-1]:
			output += ", " + str(element)
		output += "}"
		return output
	
	def to_list(self):
		return self._container[::-1]

