from touring import *
from search import *

import sys


def main():
	if len(sys.argv) < 2:	
		print("Specificare il numero di citta'.")
		return

	try:
		n = int(sys.argv[1])
		if n < 3:
			print("Il numero di citta' deve essere un numero intero positivo maggiore di 2")
			return
	except TypeError:
		print("Il numero di citta' deve essere un numero intero positivo maggiore di 2")
		return

	t0 = 20
	freezing_at = 0.1
	c = 10

	schedule = log_schedule(t0, c)
	annealing_options = {
		"max_iterations": 2**32,
		"transitions_per_temperature": 1,
		"freezing_at": freezing_at
	}

	problem = TouringProblem.random(n, 0)
	print("===== TouringProblem instance =====")
	print(f"Cities' graph:")
	for arc in problem.graph.keys():
		distance = problem.graph[arc]
		print("\t" + "-".join([str(e) for e in arc]) + ": " + str(distance))
	print()

	results = simulated_annealing(problem, schedule, **annealing_options)
	if results is None:
		print("Could not find solution!")
	else:
		solution = results
		distance = -problem.score(solution)
		print("Found solution!")
		print(f"Minimum distance is {distance}")


if __name__ == "__main__":
	main()
