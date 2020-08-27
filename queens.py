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
		points = self.n
		for column, row in enumerate(state):
			for other_column, other_row in enumerate(state):
				if column == other_column:
					continue

				dx = abs(other_column - column)
				dy = abs(other_row - row)
				if dy == 0 or dx == dy:
					points -= 1
					break
		return points
	
class MySchedule(object):
	def __init__(self, starting_temperature):
		self.temperature = starting_temperature

	def __call__(self, time):
		result = self.temperature
		self.temperature *= 0.99
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
	t0 = 3.2
	alpha = 3
	while True:
		# solution = simulated_annealing(problem, frasconi_schedule(t0, alpha), 2**33)
		solution = simulated_annealing(problem, MySchedule(100), 2**33)
		if solution is not None:
			print(f"\rFound solution: {solution}", end="")
			score = problem.score(solution)
			if score == n:
				print()
				print("===== Checkboard representation =====")
				queens = zip([i for i in range(len(solution))], solution)
				for queen in sorted(queens,  key=lambda x: x[1]):
					print("O" * (queen[0]) + "X" + "O" * (n - queen[0] - 1))
				break


if __name__ == "__main__":
	main()
