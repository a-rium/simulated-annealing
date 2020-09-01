import sys

from search import *


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


def make_arc(a, b):
	return frozenset([a, b])
		
def main():
	if len(sys.argv) < 2:	
		print("Specificare il numero di citta'.")
		return

	try:
		n = int(sys.argv[1])
		if n < 3:
			print("Il numero di citta' deve essere un numero intero positivo maggiore di 2")
			return
	except TypeError:
		print("Il numero di citta' deve essere un numero intero positivo maggiore di 2")
		return

	t0 = 20
	freezing_at = 0.1
	c = 10

	schedule = log_schedule(t0, c)
	annealing_options = {
		"max_iterations": 2**32,
		"transitions_per_temperature": 1,
		"freezing_at": freezing_at
	}

	problem = TouringProblem.random(n, 0)
	print("===== TouringProblem instance =====")
	print(f"Cities' graph:")
	for arc in problem.graph.keys():
		distance = problem.graph[arc]
		print("\t" + "-".join([str(e) for e in arc]) + ": " + str(distance))
	print()

	results = simulated_annealing(problem, schedule, **annealing_options)
	if results is None:
		print("Could not find solution!")
	else:
		solution = results
		distance = -problem.score(solution)
		print("Found solution!")
		print(f"Minimum distance is {distance}")


if __name__ == "__main__":
	main()
