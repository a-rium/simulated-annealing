from search import Problem

import collections
import random
import itertools


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
		for col, row in enumerate(board):
			diag_ne = col + row
			diag_se = (n - 1 - col) + row
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
		board = random.sample(range(n), n)
		return QueensProblem(QueensState.from_board(board))

	def action(self, state):
		return list(itertools.combinations(range(self.n), 2))

	def result(self, action, state):
		col, new_row = action
		old_row = state.board[col]
		old_diag_ne = col + old_row
		new_diag_ne = col + new_row
		old_diag_se = self.n - 1 - col + old_row
		new_diag_se = self.n - 1 - col + new_row

		new_state = state.copy()
		new_state.board[col] = new_row
		new_state.row[old_row] -= 1
		new_state.row[new_row] += 1
		new_state.northeast[old_diag_ne] -= 1
		new_state.northeast[new_diag_ne] += 1
		new_state.southeast[old_diag_se] -= 1
		new_state.southeast[new_diag_se] += 1
		return new_state

	def score(self, state):
		points = self.n
		for col, row in enumerate(state.board):
			diag_ne = col + row
			diag_se = (self.n - 1 - col) + row
			under_attack = state.row[row] > 1 or state.northeast[diag_ne] > 1 or state.southeast[diag_se] > 1
			if under_attack:
				points -= 1
		return points

	def goal(self, state):
		return self.score(state) == self.n

