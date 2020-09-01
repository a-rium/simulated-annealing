from queens import *
from search import *

import sys
import time
import argparse


class QueensProblemSchedule(LogSchedule):
	def reschedule(self, tries):
		print("Temperature has risen")
		self.temperature += 1

	
def print_checkboard(queens):
	n = len(queens)
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


def value_or_none_if_raises(f, *args, **kwargs):
	try:
		return f(*args, **kwargs)
	except:
		return None


def process_arguments(args):
	parser = argparse.ArgumentParser()
	parser.add_argument("n", type=int)
	parser.add_argument("-t", default=20, type=float)
	parser.add_argument("-c", default=10, type=float)
	parser.add_argument("--freezing-at", default=0.1, dest="freezing_at", type=float)
	parser.add_argument("--transitions-per-temperature", default=1, dest="transitions_per_temperature", type=float)
	parser.add_argument("--max-iterations", default=2**32, dest="max_iterations", type=int)
	inputs = parser.parse_args()
	if inputs.n < 4:
		print("Il numero di regine deve essere maggiore di 3")
	elif inputs.t <= 0:
		print("Initial temperature must be positive")
	else:
		return inputs


def main():
	inputs = process_arguments(sys.argv)
	if inputs is None:
		return

	options = {
		"max_iterations": inputs.max_iterations,
		"transitions_per_temperature": inputs.transitions_per_temperature,
		"freezing_at": inputs.freezing_at
	}

	print(f"Temperatura iniziale di annealing: {inputs.t}")

	make_problem = lambda: QueensProblem.random(inputs.n)
	schedule = QueensProblemSchedule(inputs.t, inputs.c)
	solution, elapsed = solve_by_simulated_annealing(make_problem, schedule, **options)
		
	print("Trovata una soluzione!")
	print("===== Rappresentazione del problema delle n regine =====")
	print(solution.board)
	print("===== Rappresentazione della scacchiera =====")
	print_checkboard(solution.board)

	timestamp = time.strftime("%H:%M:%S", time.gmtime(elapsed))
	print(f"Tempo impiegato: {timestamp}")



if __name__ == "__main__":
	main()
