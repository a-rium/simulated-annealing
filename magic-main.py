from magic import *
from search import *

import sys


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
		

def process_arguments(args):
	if len(args) < 2:
		print("Utilizzo: specificare la lunghezza del quadrato magico desiderato.")
		return None
	else:
		try:
			n = int(sys.argv[1])
			if n >= 3:
				return {"n": n}
		except:
			pass

	print("Errore: il lato deve essere un numero positivo maggiore di 2.")
	return None


def main():
	inputs = process_arguments(sys.argv)
	
	n = inputs["n"]

	t0 = 20
	freezing_at = 0.1
	c = 10

	schedule = log_schedule(t0, c)
	annealing_options = {
		"max_iterations": 2**32,
		"transitions_per_temperature": 1,
		"freezing_at": freezing_at
	}

	print(f"Temperature iniziale di annealing: {t0}")

	tries = 1
	while True:
		print(f"\rTentativo numero {tries}", end="")

		problem = MagicSquareProblem.random(n)
		solution = simulated_annealing(problem, schedule, **annealing_options)

		if solution is not None:
			tries += 1
			if problem.goal(solution):
				print()
				print("Trovata soluzione!")
				print("===== Rappresentazione della soluzione al problema =====")
				print_matrix(solution.matrix)
				break


if __name__ == "__main__":
	main()
	

