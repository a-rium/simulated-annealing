from queens import *
from search import *

import sys
import signal

	
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


Running = True
def halt_execution(sig, frame):
	global Running
	Running = False
	

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
	signal.signal(signal.SIGINT, halt_execution)
	
	walid_options = {"acceptance": 0.9, "iterations": 10**4}
	t0 = walid_initial_temperature_estimate(QueensProblem.random, n, **walid_options)
	print("Annealing temperature: {:>4}".format(t0))
	if t0 < 8:
		alpha = 2
		schedule = frasconi_schedule(t0, alpha)
	else:
		schedule = log_schedule(t0, 2)

	average_score = None
	best_score = None
	worst_score = None
	annealing_options = {"max_iterations": 2**32, "transitions_per_temperature": 1}
	average_score = None
	tries = 0
	successful_tries = 0
	while Running:
		tries += 1
		problem = QueensProblem.random(n)
		solution = simulated_annealing(problem, schedule, **annealing_options)

		if solution is not None:
			successful_tries += 1
			score = problem.score(solution)
			if average_score is not None:
				average_score = (average_score + score) / 2
			else:
				average_score = score
			if best_score is None or score > best_score:
				best_score = score
			if worst_score is None or score < worst_score:
				worst_score = score
			if problem.is_good_solution(solution):
				print()
				print("Good solution!")
				print("===== Queens Problem representation =====")
				print(solution.board)
				print("===== Checkboard representation =====")
				print_checkboard(n, solution.board)
				break

	print()
	print("==== Run-down =====")
	print(f"Tries: {tries}")
	print(f"\tSuccessful: {successful_tries}")
	print("Results' scores:")
	print(f"\tBest: {best_score}")
	print(f"\tWorst: {worst_score}")
	print(f"\tAverage: {average_score}")
	


if __name__ == "__main__":
	main()
