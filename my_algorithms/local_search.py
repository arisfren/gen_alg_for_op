from .chromosome import *
from .map import Map
from time import time

class LocalSearchModel:
	def __init__(self, map: Map):
		self.graph_size = len(map)
		self.map = map

		self.curr_path = Chromosome.from_list([1, self.graph_size])

	def insert(self, old_path: Chromosome) -> Chromosome:
		# inserts a node in a path in a best possible way
		possible_nodes = set(range(1, self.graph_size)) - set(old_path.path)
		possible_new_paths: list[Chromosome] = []
		for i in range(1, len(old_path)):
			for c in possible_nodes:
				new_path = old_path[:i] + [c] + old_path[i:]
				possible_new_paths.append(Chromosome.from_list(new_path))
		# return the best result
		return max(possible_new_paths, key=self.map.chromosome_fitness)

	def replace(self, old_path: Chromosome) -> Chromosome:
		if len(old_path) == 2:
			return old_path
		# replaces a node in a path in a best possible way
		possible_nodes = set(range(1, self.graph_size)) - set(old_path.path)
		possible_new_paths: list[Chromosome] = []
		for i in range(1, len(old_path)-1):
			for c in possible_nodes:
				new_path = old_path.path.copy()
				new_path[i] = c
				possible_new_paths.append(Chromosome.from_list(new_path))
		# return the best result
		return max(possible_new_paths, key=self.map.chromosome_fitness)

	def swap(self, old_path: Chromosome) -> Chromosome:
		if len(old_path) <= 3:
			return old_path
		# swaps two nodes in a path
		possible_new_paths: list[Chromosome] = []
		for i in range(1, len(old_path)-1):
			for j in range(i+1, len(old_path)-1):
				new_path = old_path.path.copy()
				new_path[i], new_path[j] = new_path[j], new_path[i]
				possible_new_paths.append(Chromosome.from_list(new_path))
		# return the best result
		return max(possible_new_paths, key=self.map.chromosome_fitness)

	def relocate(self, old_path: Chromosome) -> Chromosome:
		if len(old_path) == 2:
			return old_path
		# relocates a node in a path
		possible_new_paths: list[Chromosome] = []
		for i in range(1, len(old_path)-1):
			for j in range(1, len(old_path)-1):
				new_path = old_path.path.copy()
				c = new_path.pop(i)
				new_path = new_path[:j] + [c] + new_path[j:]
				possible_new_paths.append(Chromosome.from_list(new_path))
		# return the best result
		return max(possible_new_paths, key=self.map.chromosome_fitness)

	def two_opt(self, old_path: Chromosome) -> Chromosome:
		if len(old_path) <= 3:
			return old_path
		# 2-opt: replaces two archs by two other
		# 1. take route[start] to route[v1] and add them in order to new_route
		# 2. take route[v1+1] to route[v2] and add them in reverse order to new_route
		# 3. take route[v2+1] to route[start] and add them in order to new_route
		possible_new_paths: list[Chromosome] = []
		for i in range(1, len(old_path)-1):
			for j in range(i+1, len(old_path)-1):
				new_path = old_path.path[:i]
				new_path += old_path.path[j-1:i-1:-1]
				new_path += old_path.path[j:]
				possible_new_paths.append(Chromosome.from_list(new_path))
		# return the best result
		return max(possible_new_paths, key=self.map.chromosome_fitness)

	def get_new_path(self, old_path: Chromosome, methods) -> Chromosome:
		# returns the best possible path by running local search methods
		possible_new_paths = [m(old_path) for m in methods]
		new_path = max(possible_new_paths, key=self.map.chromosome_fitness)
		func_index = possible_new_paths.index(new_path)
		# print(f'function used: {methods[func_index].__name__}')
		return new_path

	def run_simulation(self, num_of_iter: int):
		t1 = time()
		possible_methods = [self.insert, self.replace, self.swap, self.relocate, self.two_opt]
		total_iter = 0
		for i in range(num_of_iter):
			# removes methods that require partial path
			if i == self.graph_size-2:
				possible_methods.remove(self.insert)
				possible_methods.remove(self.replace)

			new_path = self.get_new_path(self.curr_path, possible_methods)
			# stops when solution have been found
			if self.map.path_distance(self.curr_path) >= self.map.path_distance(new_path):
				self.curr_path = new_path
				break

			# print(f'iter {i}: '
			# 	  # f'\t score: {self.chromosome_fitness(best):.4f}, '
			# 	  f'\t dist: {self.map.path_distance(new_path):.4f}'
			# 	  f'\t path: {new_path}')
			self.curr_path = new_path
			total_iter = i

		t2 = time()
		print(f'LS: best solution found after {total_iter} iterations ({t2 - t1:.5f}s)'
			  f'\n\t dist: {self.map.path_distance(self.curr_path):.4f}'
			  f'\n\t path: {self.curr_path}'
			  f'\n\t num of nodes: {len(self.curr_path)}')


