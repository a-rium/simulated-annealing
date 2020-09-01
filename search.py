import math
import random
import time



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

	def goal(self, state):
		pass


class LogSchedule(object):
	def __init__(self, initial_temperature, speedup):
		self.temperature = initial_temperature
		self.speedup = speedup

	def __call__(self, t):
		return self.temperature / (self.speedup * math.log2(1 + t))
	
	def reschedule(self, tries):
		pass


def solve_by_simulated_annealing(make_problem, schedule, **options):
	tries = 1
	start = time.time()
	while True:
		problem = make_problem()
		solution = simulated_annealing(problem, schedule, **options)

		if solution is not None:
			if problem.goal(solution):
				end = time.time()
				break

		tries += 1
		schedule.reschedule(tries)
				

	return solution, end - start
	

def simulated_annealing(problem, schedule, *, transitions_per_temperature=1, max_iterations=10**6, freezing_at=0.5):
	current = Node(problem.initial_state, problem.score(problem.initial_state))
	for time in range(1, max_iterations + 1):
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
	

def exp_schedule(k, λ, limit):
	""" Funzione di schedule riportata sul libro R&N """
	def schedule(t):
		if t < limit:
			return k * math.exp(-λ * t)
		else:
			return 0

	return schedule


def log_schedule(t0, speedup):
	def schedule(t):
		return t0 / (speedup * math.log2(1 + t))

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
