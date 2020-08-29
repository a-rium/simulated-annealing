from search import *

import sys
import collections
import signal


class QueensState(object):
	def __init__(self, board, row, northeast, southeast):
		self.board = board
		self.row = row
		self.northeast = northeast
		self.southeast = southeast

	@classmethod
	def from_board(cls, board):
		n = len(board)
		state_row = collections.defaultdict(lambda: 0)
		northeast = collections.defaultdict(lambda: 0)
		southeast = collections.defaultdict(lambda: 0)
		for column, row in enumerate(board):
			diag_ne = column + row
			diag_se = n - 1 - column + row
			state_row[row] += 1
			northeast[diag_ne] += 1
			southeast[diag_se] += 1
		return QueensState(board, state_row, northeast, southeast)

	def copy(self):
		board = self.board.copy()
		row = self.row.copy()
		northeast = self.northeast.copy()
		southeast = self.southeast.copy()
		return QueensState(board, row, northeast, southeast)


class QueensProblem(Problem):
	def __init__(self, state):
		self.n = len(state.board)
		super().__init__(state)

	@classmethod
	def default(cls, n):
		board = [0] * n
		return QueensProblem(QueensState.from_board(board))

	@classmethod
	def random(cls, n):
		board = [random.randint(0, n - 1) for i in range(n)]
		return QueensProblem(QueensState.from_board(board))

	def action(self, state):
		return [(c, r) for r in range(self.n) for c in range(self.n) if c != r]

	def result(self, action, state):
		column, new_row = action
		old_row = state.board[column]
		old_diag_ne = column + old_row
		new_diag_ne = column + new_row
		old_diag_se = self.n - 1 - column + old_row
		new_diag_se = self.n - 1 - column + new_row

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
			diag_ne = column + row
			diag_se = self.n - 1 - column + row
			if state.row[row] > 1 or state.northeast[diag_ne] > 1 or state.southeast[diag_se] > 1:
				points -= 1
		return points

	def is_good_solution(self, state):
		return self.score(state) == self.n

	
def modified_frasconi_schedule(t0, alpha):
	import math
	def schedule(t):
		den = math.log2(t0 + alpha)
		return t0 / (den * den)
	return schedule


def print_checkboard(n, queens):
	empty = " "
	queen_marker = "X"
	hline = "+" + ("-+" * n)
	queens_positions_ordered_by_column = sorted(enumerate(queens), key=lambda x: x[1])
	for column, _ in queens_positions_ordered_by_column:
		print(hline)
		pre_marker = "|" + (empty + "|") * column
		after_marker  = "|" + (empty + "|") * (n - column - 1)
		print(pre_marker + queen_marker + after_marker)
	print(hline)


Running = True
def halt_execution(sig, frame):
	global Running
	Running = False
	

def main():
	if len(sys.argv) < 2:
		print("Specificare N")
		return

	try:
		n = int(sys.argv[1])
		if n <= 3:
			print("N deve essere un numero intero positivo maggiore di 3")
			return
	except TypeError:
		print("N deve essere un numero intero positivo")
		return

	signal.signal(signal.SIGINT, halt_execution)
	
	walid_options = {"acceptance": 0.95, "iterations": 10**4}
	t0 = 10
	# t0 = walid_initial_temperature_estimate(QueensProblem.random, n, **walid_options)
	print("Annealing temperature: {:>4}".format(t0))
	if t0 < 8:
		alpha = 2
		schedule = frasconi_schedule(t0, alpha)
	else:
		schedule = log_schedule(t0, 2)

	# schedule = exp_schedule(20, 0.001, 100)

	raise_temperature_after = 20

	average_score = None
	best_score = None
	worst_score = None
	annealing_options = {"max_iterations": 2**32, "transitions_per_temperature": 1}
	average_score = None
	tries = 0
	successful_tries = 0
	while Running:
		tries += 1
		problem = QueensProblem.random(n)
		solution = simulated_annealing(problem, schedule, **annealing_options)

		if solution is not None:
			successful_tries += 1
			score = problem.score(solution)
			if average_score is not None:
				average_score = (average_score + score) / 2
			else:
				average_score = score
			if best_score is None or score > best_score:
				best_score = score
			if worst_score is None or score < worst_score:
				worst_score = score
			if problem.is_good_solution(solution):
				print()
				print("Good solution!")
				print("===== Queens Problem representation =====")
				print(solution.board)
				print("===== Checkboard representation =====")
				print_checkboard(n, solution.board)
				break
			elif tries % raise_temperature_after == 0:
				pass
	print()
	print("==== Run-down =====")
	print(f"Tries: {tries}")
	print(f"\tSuccessful: {successful_tries}")
	print("Results' scores:")
	print(f"\tBest: {best_score}")
	print(f"\tWorst: {worst_score}")
	print(f"\tAverage: {average_score}")
	


if __name__ == "__main__":
	main()
