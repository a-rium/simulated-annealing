from touring import *
from search import *

import sys
import time


def print_graph(graph, prefix=""):
	with open("graph.tsp", "w") as f:
		for arc in graph:
			weight = graph[arc]
			arc_representation = "-".join([str(e) for e in arc])
			f.write(f"{prefix}{arc_representation}: {weight}\n")


def main():
	inputs = process_arguments(sys.argv)
	if inputs is None:
		return
	elif inputs.n < 3:
		print("Errore: il numero di citta' deve essere maggiore di 2")
		return

	options = {
		"max_iterations": inputs.max_iterations,
		"transitions_per_temperature": inputs.transitions_per_temperature,
		"freezing_at": inputs.freezing_at
	}

	print(f"Temperatura iniziale di annealing: {inputs.t}")

	problem = TouringProblem.random(inputs.n, 0)
	print("===== Istanza di TouringProblem =====")
	print(f"Grafo delle citta':")
	print_graph(problem.graph, "\t")

	start = time.time()
	schedule = log_schedule(inputs.t, inputs.c)
	solution = simulated_annealing(problem, schedule, **options)
	if solution is not None:
		end = time.time()
		distance = -problem.score(solution)
		print("Trovata una soluzione!")
		print(f"La distanza minima da percorrere e' {distance}")

		path = [str(city) for city in solution]
		print(f"Percorso: " + ", ".join(["0", *path]))
	else:
		print("Non e' stato possibile trovare una soluzione")
	
	elapsed = end - start
	timestamp = time.strftime("%H:%M:%S", time.gmtime(elapsed))
	print(f"Tempo impiegato: {timestamp}")



if __name__ == "__main__":
	main()
