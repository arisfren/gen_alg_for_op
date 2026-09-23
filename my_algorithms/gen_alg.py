from .chromosome import *
from .map import Map
from time import time


class GeneticAlgorithm:
	crossover_prob: float = 1.0
	mutation_prob: float = 0.1
	alpha: float = 4
	max_iter_without_improvement = 20

	def __init__(self, map: Map, pop_size: int):
		self.graph_size = len(map)
		self.pop_size = pop_size
		self.map = map

		self.curr_population: list[Chromosome] = self.initial_population()

	@property
	def best_chromosome(self):
		return max(self.curr_population, key=self.map.chromosome_fitness)

	def initial_population(self) -> list[Chromosome]:
		# create random chromosomes
		pop = [Chromosome(self.graph_size) for _ in range(self.pop_size)]

		# how many chromosomes have distance less than max
		count = sum([1 for c in pop if self.map.path_distance(c) <= self.map.max_distance])

		point_ommision_prob = 1 - count / self.pop_size

		# omit points
		new_pop: list[Chromosome]= []
		for c in pop:
			new_path = [(0 if random.random() < point_ommision_prob else p) for p in c.path[1:-1]]
			new_path = [v for v in new_path if v != 0]
			new_pop.append(Chromosome.from_list([1] + new_path + [self.graph_size]))

		return new_pop

	def calculate_next_population(self) -> list[Chromosome]:
		# cross and mutate offsprings
		offsprings = self.crossover(self.curr_population)
		offsprings = self.mutation(offsprings)

		# evaluate and select
		new_population = self.selection(self.curr_population + offsprings)
		return new_population

	def tournament_selection(self, population: list[Chromosome], out_size: int, k: int = 2):
		out_list = []
		for _ in range(out_size):
			# perform a tournament of size k
			tournament: list[Chromosome] = random.sample(population, k)
			best_chromosome = max(tournament, key=self.map.chromosome_fitness)
			out_list.append(best_chromosome)
		return out_list

	def crossover(self, population: list[Chromosome]) -> list[Chromosome]:
		num_of_parents = int(len(population) * self.crossover_prob) // 2 * 2
		# select parents using tournament selection of size 2
		parents = self.tournament_selection(population, num_of_parents)
		children = [scx(parents[i], parents[i + 1], self.map.profits) for i in range(num_of_parents // 2)]
		return children

	def mutation(self, parents: list[Chromosome]) -> list[Chromosome]:
		num_of_paretns = int(len(parents) * self.mutation_prob)

		children = []
		for i in range(num_of_paretns):
			# 2-opt
			child = mutation_two_opt(parents[i], self.map.chromosome_fitness)
			# add a point
			while True:
				new_child = mutation_add_point(child)
				if self.map.path_distance(new_child) < self.map.max_distance:
					child = new_child
				else:
					break
			children.append(child)

		return children

	def selection(self, population: list[Chromosome]) -> list[Chromosome]:
		# selection uses tournament selection of size 2
		return self.tournament_selection(population, self.pop_size)

	def run_simulation(self, num_of_iterations: int):
		t1 = time()
		total_iter = 0
		num_of_stagnant_iter = 0
		for i in range(num_of_iterations):
			prev_best = self.best_chromosome
			print(f'iter {i}: '
				  # f'\t score: {self.chromosome_fitness(best):.4f}, '
				  f'\t dist: {self.map.path_distance(prev_best):.4f} '
				  f'best: {prev_best}')
			self.curr_population = self.calculate_next_population()

			# stop the simulation if the best solution doesnt change
			if self.map.chromosome_fitness(self.best_chromosome) <= self.map.chromosome_fitness(prev_best):
				num_of_stagnant_iter += 1
			else:
				num_of_stagnant_iter = 0
			if num_of_stagnant_iter == self.max_iter_without_improvement:
				break

			total_iter = i
		t2 = time()

		print(f'GA: best solution found in {total_iter} iterations ({t2-t1:.5f}s):'
			  f'\n\t time: {self.map.path_distance(self.best_chromosome)/3600:.4f}'
			  f'\n\t profit: {self.map.path_profit(self.best_chromosome)}'
			  # f'\n\t path: {self.best_chromosome}'
			  f'\n\t num of nodes: {sum([bool(i) for i in self.best_chromosome])}')
