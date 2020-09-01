from search import Problem

import collections
import random


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
			under_attack = state.row[row] > 1 or state.northeast[diag_ne] > 1 or state.southeast[diag_se] > 1
			if under_attack:
				points -= 1
		return points

	def is_good_solution(self, state):
		return self.score(state) == self.n

