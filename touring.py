from search import *

class TouringState(Problem):
	def __init__(self, current, visited, distance):
		self.current = current
		self.visited = visited
		self.distance = distance


class CitiesGraph(object):
	def __init__(self, cities, cities_graph):
		self.cities = cities
		self.cities_graph = cities_graph


class TouringProblem(Problem):
	def __init__(self, starting_from, cities_graph):
		self.starting_from = city
		self.cities_graph = cities_graph
		root = Node(TouringState(starting_from, {}, 0)
		super().__init__(root, 0)
	
	def action(self, state):
		return self.cities_graph.cities - state.visited

	def result(self, action, state):
		distance = self.cities_graph.distance[{action, state}]
		return TouringState(action, state.visited + action, self.distance + distance)

	def score(self, state):
		return -state.distance


		
def main():
	cities = [i for i in range(4)]
	distance = {
	{0, 1}: 4,
	{0, 2}: 2,
	{0, 3}: 6,
	{1, 2}: 2,
	{1, 3}: 3,
	{2, 3}: 1
	}

	graph = CitiesGraph(cities, distance)
	problem = TouringProblem(0, graph)

	solution = simulated_annealing(problem, frasconi_scheduler(1.6. 3), 2**32)
	if solution is None:
		print("Could not find solution!")
	else:
		print("Found solution!")
		print(f" -> {solution}")


if __name__ == "__main__":
	main()
