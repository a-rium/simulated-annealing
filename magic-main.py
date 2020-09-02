from magic import *
from search import *

import sys
import time


class MagicSquareSchedule(LogSchedule):
	def reschedule(self, tries):
		if tries == 10:
			self.temperature += 1
			print(f"Riprogrammazione: la temperatura iniziale e' {self.temperature}")
		

def print_matrix(matrix):
	n = len(matrix)
	padding = len(str(n**2))
	padding_format = "{:>" + str(padding) + "}"
	hline = "+" + ((("-" * padding) + "+") * n)
	for row in matrix:
		print(hline)
		print("|", end="")
		for e in row:
			print((padding_format + "|").format(e), end="")
		print()
	print(hline)
		

def main():
	inputs = process_arguments(sys.argv)
	if inputs is None:
		return
	elif inputs.n < 3:
		print("Errore: la lunghezza del lato deve essere maggiore di 2")
		return


	options = {
		"max_iterations": inputs.max_iterations,
		"transitions_per_temperature": inputs.transitions_per_temperature,
		"freezing_at": inputs.freezing_at
	}

	print(f"Temperature iniziale di annealing: {inputs.t}")

	make_problem = lambda: MagicSquareProblem.random(inputs.n)
	schedule = MagicSquareSchedule(inputs.t, inputs.c)
	solution, elapsed = solve_by_simulated_annealing(make_problem, schedule, **options)
	
	print("Trovata soluzione!")
	print("===== Rappresentazione della soluzione al problema =====")
	print_matrix(solution.matrix)

	timestamp = time.strftime("%H:%M:%S", time.gmtime(elapsed))
	print(f"Tempo impiegato: {timestamp}")


if __name__ == "__main__":
	main()
	

