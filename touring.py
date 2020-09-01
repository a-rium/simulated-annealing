from search import Problem

import random
import itertools


class TouringProblem(Problem):
	def __init__(self, n, starting_city, path, graph):
		self.starting_city = starting_city
		self.graph = graph
		super().__init__(path)
	
	@classmethod
	def random(cls, n, starting_city):
		path = [i for i in range(n) if i != starting_city]
		random.shuffle(path)
		arcs = itertools.combinations(range(n), 2)
		graph = {frozenset(arc): random.randint(1, n) for arc in arcs}
		return TouringProblem(n, starting_city, path, graph)
		
	def action(self, state):
		return list(itertools.combinations(range(len(state)), 2))

	def result(self, action, state):
		a, b = action
		new_path = state.copy()
		new_path[a], new_path[b] = new_path[b], new_path[a]
		return new_path

	def score(self, state):
		arc = frozenset((self.starting_city, state[0]))
		distance = self.graph[arc]
		for i in range(len(state) - 1):
			arc = frozenset((state[i], state[i + 1]))
			distance += self.graph[arc]
		arc = frozenset((self.starting_city, state[-1]))
		distance += self.graph[arc]
		return -distance
