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
		if temperature < 0.5:
			return current.state

		action = random.choice(problem.action(current.state))
		state = problem.result(action, current.state)
		candidate  = Node(state, problem.score(state))
		gain = candidate.score - current.score
		if gain > 0 or random.random() < math.exp( gain / temperature):
			current = candidate

	return None


def frasconi_schedule(t0, alpha):
	def schedule(t):
		return t0 / math.log2(t + alpha)

	return schedule
	
