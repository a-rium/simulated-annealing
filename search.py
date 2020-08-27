import math
import random



class Node(object):
	def __init__(self, state, score):
		self.state = state
		self.score = score


class Problem(object):
	def __init__(self, initial_state):
		self.initial_state = initial_state

	def action(self, state):
		pass

	def result(self, action, state):
		pass

	def score(self, state):
		pass


def simulated_annealing(problem, schedule, max_iterations):
	current = Node(problem.initial_state, problem.score(problem.initial_state))
	for time in range(max_iterations):
		temperature = schedule(time)
		# print(f"temperature is: {temperature}")
		if temperature < 0.01:
			return current.state

		actions = problem.action(current.state)
		# print(actions)
		neighbour_states = [problem.result(action, current.state) for action in actions]
		neighbour_nodes = [Node(state, problem.score(state)) for state in neighbour_states]
		candidate = random.choice(neighbour_nodes)
		gain = candidate.score - current.score
		if gain > 0 or random.random() < math.exp( gain / temperature):
			current = candidate

	print(f"temperature is: {temperature}")
	return None


def frasconi_schedule(t0, alpha):
	def schedule(t):
		return t0 / math.log2(t + alpha)

	return schedule
	
