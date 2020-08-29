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


def walid_initial_temperature_estimate(make_random_problem, *args, acceptance, iterations, ε=0.001):
	""" 
	Estimates the initial temperature needed so that the acceptance ratio is as requested
	using Walid's algorithm (see

	https://www.researchgate.net/publication/227061666_Computing_the_Initial_Temperature_of_Simulated_Annealing

	for a more detailed explanation).
	"""

	i = 0
	scores = []
	while i < iterations:
		problem = make_random_problem(*args)
		current = Node(problem.initial_state, problem.score(problem.initial_state))
		action = random.choice(problem.action(current.state))
		state = problem.result(action, current.state)
		candidate  = Node(state, problem.score(state))
		gain = candidate.score - current.score
		if gain < 0:
			scores.append((candidate.score, current.score))
			i += 1
	
	def χ_hat(T):
		num = sum([math.exp(-score[0] / T) for score in scores])
		den = sum([math.exp(-score[1] / T) for score in scores])

		return num / den
	
	t0 = 1
	log_acceptance = math.log(acceptance)
	while True:
		estimate = χ_hat(t0)
		if abs(acceptance - estimate) < ε:
			return -t0
		else:
			t0 = t0 * ((math.log(estimate) / log_acceptance))


def simulated_annealing(problem, schedule, *, transitions_per_temperature=1, max_iterations=10**6, freezing_at=0.5):
	current = Node(problem.initial_state, problem.score(problem.initial_state))
	for time in range(max_iterations):
		temperature = schedule(time)
		if temperature < freezing_at:
			return current.state

		for _ in range(transitions_per_temperature):
			action = random.choice(problem.action(current.state))
			state = problem.result(action, current.state)
			candidate  = Node(state, problem.score(state))
			gain = candidate.score - current.score
			if gain > 0 or random.random() < math.exp(gain / temperature):
				current = candidate

	return None


def frasconi_schedule(t0, alpha):
	def schedule(t):
		return t0 / math.log2(t + alpha)

	return schedule
	

def log_schedule(t0, speedup):
	def schedule(t):
		return t0 / (speedup * math.log2(1.1 + t))

	return schedule


def linear_schedule(t0, a, b):
	class Schedule(object):
		def __init__(self):
			self.temperature = t0

		def __call__(self, time):
			result = self.temperature
			self.temperature *= a
			self.temperature -= b
			return result

	return Schedule()


def geometric_schedule(t0, a):
	return linear_schedule(t0, a, 0)


def arithmetic_schedule(t0, b):
	return linear_schedule(t0, 1, b)
