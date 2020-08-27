from search import *

import sys


class QueensProblem(Problem):
	def __init__(self, n):
		self.n = n
		super().__init__([0] * n)

	def action(self, state):
		moves = []
		for column, row in enumerate(state):
			if row > 0:
				moves.append((column, row - 1))
			if row < self.n - 1:
				moves.append((column, row + 1))
		return moves

	def result(self, action, state):
		new_state = state.copy()
		new_state[action[0]] = action[1]
		return new_state

	def score(self, state):
		under_attack = set()
		for column, row in enumerate(state[:-1]):
			for other_column, other_row in enumerate(state[column + 1:], column + 1):
				dx = other_column - column
				dy = abs(other_row - row)
				if dy == 0 or dx == dy:
					under_attack.add(column)
					under_attack.add(other_column)
		return self.n - len(under_attack)

	
class MySchedule(object):
	def __init__(self, starting_temperature):
		self.temperature = starting_temperature

	def __call__(self, time):
		result = self.temperature
		self.temperature *= 0.999
		return result
		

def main():
	if len(sys.argv) < 2:
		print("Specificare N")
		exit()

	try:
		n = int(sys.argv[1])
	except TypeError:
		print("N deve essere un numero intero positivo")
	
	problem = QueensProblem(n)
	t0 = 2
	alpha = 3
	tries = 0
	raise_temperature_after = 20
	while True:
		print("\rAnnealing temperature: {:>4}, try no. {:>6}".format(t0, tries), end="")
		solution = simulated_annealing(problem, frasconi_schedule(t0, alpha), 2**33)
		# solution = simulated_annealing(problem, MySchedule(100), 2**33)
		if solution is not None:
			tries += 1
			score = problem.score(solution)
			if score == n:
				print()
				print("Good solution!")
				print("===== Checkboard representation =====")
				queens = zip([i for i in range(len(solution))], solution)
				for queen in sorted(queens,  key=lambda x: x[1]):
					print("O" * (queen[0]) + "X" + "O" * (n - queen[0] - 1))
				break
			elif tries % raise_temperature_after == 0:
				t0 += 1


if __name__ == "__main__":
	main()
