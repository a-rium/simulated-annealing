from magic import *
from search import *

import sys


def print_matrix(matrix):
	n = len(matrix)
	padding = ((n**2) // 10) + 1
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
	if len(sys.argv) < 2:	
		print("Specificare il lato del quadrato magico desiderato.")
		return

	try:
		n = int(sys.argv[1])
		if n < 2:
			print("Il lato deve avere lunghezza maggiore o uguale a 2")
			return
	except TypeError:
		print("Il lato deve essere un numero intero positivo")
		return

	t0 = walid_initial_temperature_estimate(MagicSquareProblem.random, n, acceptance=0.92, iterations=10**4)
	if t0 < 8:
		alpha = 2
		schedule = frasconi_schedule(t0, alpha)
	elif t0 < 11:
		schedule = log_schedule(t0, 2)
	else:
		schedule = log_schedule(t0, 5)

	tries = 1
	raise_temperature_after = 20
	while True:
		print("\rAnnealing temperature: {:>4}, try no. {:>6}, score ".format(t0, tries), end="")

		problem = MagicSquareProblem.random(n)
		solution = simulated_annealing(problem, schedule, transitions_per_temperature=2, max_iterations=2**32)

		if solution is not None:
			tries += 1
			score = problem.score(solution)
			print("{:>3}".format(score), end="")
			if score == 0:
				print()
				print("Good solution!")
				print("===== Magic Square Problem representation =====")
				print_matrix(solution.matrix)
				break
			elif tries % raise_temperature_after == 0:
				pass


if __name__ == "__main__":
	main()
	

