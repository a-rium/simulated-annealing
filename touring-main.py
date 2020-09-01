from touring import *
from search import *

import sys


def process_arguments(args):
	if len(args) < 2:
		print("Utilizzo: passare il numero di citta'.")
		return None
	else:
		try:
			n = int(sys.argv[1])
			if n > 3:
				return {"n": n}
		except:
			pass

	print("Errore: il numero di citta' deve essere un numero intero positivo maggiore di 2")
	return None


def print_graph(graph, prefix=""):
	for arc in graph:
		weight = graph[arc]
		arc_representation = "-".join([str(e) for e in arc])
		print(f"{prefix}{arc_representation}: {weight}")


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

	problem = TouringProblem.random(n, 0)
	print("===== TouringProblem instance =====")
	print(f"Cities' graph:")
	print_graph(problem.graph, "\t")

	solution = simulated_annealing(problem, schedule, **annealing_options)
	if solution is not None:
		distance = -problem.score(solution)
		print("Found solution!")
		print(f"Minimum distance is {distance}")
	else:
		print("Could not find solution!")


if __name__ == "__main__":
	main()
