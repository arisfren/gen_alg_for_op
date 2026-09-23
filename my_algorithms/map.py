from .chromosome import Chromosome
from math import pow


class Map:
	def __init__(self, distance_matrix: list[list[float]], profits: list[float], costs: list[float], max_distance = 10**6) -> None:
		if len(distance_matrix) != len(profits):
			raise ValueError("distance matrix and profits have to be of the same dimention!")

		self.distance_matrix = distance_matrix
		self.profits = profits
		self.costs = costs
		self.max_distance = max_distance
		self.alpha = 4

	def path_distance(self, path: list[int] | Chromosome) -> float:
		distance = 0.
		for i in range(len(path)-1):
			distance += self.distance_matrix[path[i] - 1][path[i+1] - 1]
			distance += self.costs[path[i] - 1]
		return distance

	def path_profit(self, path: list[int] | Chromosome) -> float:
		return sum([self.profits[i-1] for i in path])

	def chromosome_fitness(self, c: Chromosome) -> float:
		# fitness = profit
		return self.path_profit(c) * self.penality(c)

	def penality(self, c: Chromosome) -> float:
		return pow(self.max_distance / self.path_distance(c), self.alpha) \
			if self.path_distance(c) > self.max_distance else 1

	def __len__(self) -> int:
		return len(self.profits)
