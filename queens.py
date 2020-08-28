from search import *

import sys
import collections


class QueensState(object):
	def __init__(self, board, row, northeast, southeast):
		self.board = board
		self.row = row
		self.southeast = southeast
		self.northeast = northeast

	def copy(self):
		board = self.board.copy()
		row = self.row.copy()
		northeast = self.northeast.copy()
		southeast = self.southeast.copy()
		return QueensState(board, row, northeast, southeast)


class QueensProblem(Problem):
	def __init__(self, n):
		self.n = n
		board = [0] * n
		row = collections.defaultdict(lambda: 0)
		northeast = collections.defaultdict(lambda: 0)
		southeast = collections.defaultdict(lambda: 0)
		row[0] = n
		for i in range(n):
			northeast[i] = 1
			southeast[n - 1 + i] = 1
		super().__init__(QueensState(board, row, northeast, southeast))

	def action(self, state):
		moves = []
		for column, row in enumerate(state.board):
			if row > 0:
				moves.append((column, row - 1))
			if row < self.n - 1:
				moves.append((column, row + 1))
		return moves

	def result(self, action, state):
		column, new_row = action
		old_row = state.board[column]
		old_diag_ne = column + old_row
		new_diag_ne = column + new_row
		old_diag_se = self.n - 1 + (column - old_row)
		new_diag_se = self.n - 1 + (column - new_row)

		new_state = state.copy()
		new_state.board[column] = new_row
		new_state.row[old_row] -= 1
		new_state.row[new_row] += 1
		new_state.northeast[old_diag_ne] -= 1
		new_state.northeast[new_diag_ne] += 1
		new_state.southeast[old_diag_se] -= 1
		new_state.southeast[new_diag_se] += 1
		return new_state

	def score(self, state):
		points = self.n
		for column, row in enumerate(state.board):
			diag = column + row
			if state.row[row] > 1 or state.northeast[diag] > 1 or state.southeast[diag] > 1:
				points -= 1
		return points

	
class MySchedule(object):
	def __init__(self, starting_temperature):
		self.temperature = starting_temperature

	def __call__(self, time):
		result = self.temperature
		self.temperature *= 0.99
		return result
		

def modified_frasconi_schedule(t0, alpha):
	import math
	def schedule(t):
		den = math.log2(t0 + alpha)
		return t0 / (den * den)
	return schedule


def print_checkboard(n, queens_rows):
	queens_columns = range(len(queens_rows))
	queens = zip(queens_columns, queens_rows)
	empty = " "
	occupied = "X"
	for queen in sorted(queens,  key=lambda x: x[1]):
		print("+" + ("-+" * n))
		pre_queen = queen[0]
		after_queen  = n - queen[0] - 1
		print("|" +  (f"{empty}|" * pre_queen) + f"{occupied}|" + (f"{empty}|" * after_queen))
	print("+" + ("-+" * n))


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
		# solution = simulated_annealing(problem, modified_frasconi_schedule(t0, alpha), 2**33)
		# solution = simulated_annealing(problem, MySchedule(t0), 2**33)
		if solution is not None:
			tries += 1
			score = problem.score(solution)
			if score == n:
				print()
				print("Good solution!")
				print("===== Queens Problem representation =====")
				print(solution.board)
				print("===== Checkboard representation =====")
				print_checkboard(n, solution.board)
				break
			elif tries % raise_temperature_after == 0:
				t0 += 1


if __name__ == "__main__":
	main()
