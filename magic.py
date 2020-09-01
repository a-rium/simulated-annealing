from search import Problem

import random


class MagicSquareState():
	def __init__(self, matrix, hsums, vsums, nedsums, sedsums, positions):
		self.matrix = matrix
		self.hsums = hsums
		self.vsums = vsums
		self.nedsums = nedsums
		self.sedsums = sedsums
		self.positions = positions

	@classmethod
	def from_matrix(cls, matrix):
		n = len(matrix)
		hsums = [0] * n
		vsums = [0] * n
		nedsums = 0
		sedsums = 0
		positions = {}
		for i, row in enumerate(matrix):
			positions = {**positions, **{e: (i, j) for j, e in enumerate(row)}}
			hsums[i] = sum(row)
			vsums = [vsums[j] + row[j] for j in range(len(row))]
			nedsums += matrix[i][i]
			sedsums += matrix[i][n - 1 - i]
		return MagicSquareState(matrix, hsums, vsums, nedsums, sedsums, positions)

	def copy(self):
		matrix = [row.copy() for row in self.matrix]
		hsums = self.hsums.copy()
		vsums = self.vsums.copy()
		positions = self.positions.copy()
		return MagicSquareState(matrix, hsums, vsums, self.nedsums, self.sedsums, positions)


class MagicSquareProblem(Problem):
	moves = {}

	def __init__(self, state):
		self.n = len(state.matrix)
		self.magic_constant = self.n * (self.n**2 + 1) / 2
		if self.n not in MagicSquareProblem.moves:
			nrange = range(self.n)
			MagicSquareProblem.moves[self.n] = [((a, b), (c, d)) for a in nrange for b in nrange for c in nrange for d in nrange]
		super().__init__(state)
	
	@classmethod
	def random(cls, n):
		numbers = [z for z in range(1, n**2 + 1)]
		random.shuffle(numbers)
		matrix = [[z for z in numbers[i*n:(i+1)*n]] for i in range(n)]
		return MagicSquareProblem(MagicSquareState.from_matrix(matrix))

	def action2(self, state):
		return MagicSquareProblem.moves[self.n]

	def action(self, state):
		return [(state.positions[i], state.positions[i+1]) for i in range(1, self.n**2)]
	
	def result(self, action, state):
		from_row, from_col = action[0]
		to_row, to_col = action[1]

		from_square = state.matrix[from_row][from_col]
		to_square = state.matrix[to_row][to_col]

		from_diff = to_square - from_square
		to_diff = from_square - to_square

		new_state = state.copy()
		new_state.positions[from_square] = action[1]
		new_state.positions[to_square] = action[0]
		new_state.matrix[from_row][from_col] = to_square
		new_state.matrix[to_row][to_col] = from_square
	
		new_state.hsums[from_row] += from_diff
		new_state.vsums[from_col] += from_diff
		new_state.hsums[to_row] += to_diff
		new_state.vsums[to_col] += to_diff

		if from_row == from_col:
			new_state.nedsums += from_diff
		if from_row == self.n - 1 - from_col:
			new_state.sedsums += from_diff
		if to_row == to_col:
			new_state.nedsums += to_diff
		if to_row == self.n - 1 - to_col:
			new_state.sedsums += to_diff

		return new_state

	def score(self, state):
		points = sum([abs(self.magic_constant - s) for s in state.hsums])
		points += sum([abs(self.magic_constant - s) for s in state.vsums])
		points += 0 if state.nedsums == self.magic_constant else 1
		points += 0 if state.sedsums == self.magic_constant else 1
		return -points

	def score2(self, state):
		points = state.hsums.count(self.magic_constant)
		points += state.vsums.count(self.magic_constant)
		points += 1 if state.nedsums == self.magic_constant else 0
		points += 1 if state.sedsums == self.magic_constant else 0
		return points

