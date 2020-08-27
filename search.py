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
		if temperature == 0:
			return current.state

		successors = [problem.result(a, current.state) for a in problem.action(current.state)]
		candidate = random.choice(successors)
		score_difference = candidate.score - current.score
		if score_difference > 0 or random.random() < math.exp(score_difference / temperature):
			current = candidate

	return None
