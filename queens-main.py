from queens import *
from search import *

import sys
import time

	
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


def process_arguments(args):
	if len(args) < 2:
		print("Utilizzo: passare la lunghezza del lato della scacchiera 'n' (n > 3)")
		return None
	else:
		try:
			n = int(sys.argv[1])
			if n > 3:
				return {"n": n}
		except:
			pass

	print("Errore: n deve essere un numero intero positivo maggiore di 3")
	return None


def main():
	inputs = process_arguments(sys.argv)
	if inputs is None:
		return

	n = inputs['n']
	
	t0 = 20
	freezing_at = 0.1
	c = 10

	schedule = log_schedule(t0, c)
	annealing_options = {
		"max_iterations": 2**32,
		"transitions_per_temperature": 1,
		"freezing_at": freezing_at
	}

	print(f"Temperatura iniziale di annealing: {t0}")

	tries = 0
	start = time.time()
	while True:
		tries += 1
		print(f"\rTentativo numero {tries}", end="")

		problem = QueensProblem.random(n)
		solution = simulated_annealing(problem, schedule, **annealing_options)

		if solution is not None:
			if problem.goal(solution):
				end = time.time()
				print()
				print("Trovata una soluzione!")
				print("===== Rappresentazione del problema delle n regine =====")
				print(solution.board)
				print("===== Rappresentazione della scacchiera =====")
				print_checkboard(n, solution.board)
				break

	timestamp = time.strftime("%H:%M:%S", time.gmtime(end - start))
	print(f"Tempo impiegato: {timestamp}")


if __name__ == "__main__":
	main()
