from search import Problem

import random


def make_arc(a, b):
	return frozenset([a, b])


class TouringState(Problem):
	def __init__(self, current, visited, distance):
		self.current = current
		self.visited = visited
		self.distance = distance


class CitiesGraph(object):
	def __init__(self, cities, distances):
		self.cities = cities
		self.distances = distances


class TouringProblem(Problem):
	def __init__(self, n, starting_city, path, graph):
		self.n = n
		self.starting_city = starting_city
		self.graph = graph
		super().__init__(path)
	
	@classmethod
	def random(cls, n, starting_city):
		path = [i for i in range(n) if i != starting_city]
		random.shuffle(path)
		graph = {make_arc(i, j): random.randint(1, n) for i in range(n) for j in range(n) if i != j}
		return TouringProblem(n, starting_city, path, graph)
		
	def action(self, state):
		nrange = range(self.n - 1)
		return [(i, j) for i in nrange for j in nrange if i != j]

	def result(self, action, state):
		a, b = action
		new_path = state.copy()
		new_path[a], new_path[b] = new_path[b], new_path[a]
		return new_path

	def score(self, state):
		distance = self.graph[make_arc(self.starting_city, state[0])]
		for i in range(self.n - 2):
			distance += self.graph[make_arc(state[i], state[i + 1])]
		distance += self.graph[make_arc(self.starting_city, state[-1])]
		return -distance
