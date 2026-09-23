import random

class Chromosome:
	def __init__(self, n: int):
		self.n = n
		self.path: list[int] = self.generate_random_path(n)

	@classmethod
	def from_list(cls, path: list[int]):
		obj = cls(max(path))
		obj.path = path
		return obj

	def generate_random_path(self, n) -> list[int]:
		# path representation, without zeros
		if n == 2:
			return [1, n]

		random_n = random.randint(2, n - 1)  # last point
		random_path = list(range(2, random_n+1))
		random.shuffle(random_path)
		return [1] + random_path + [n]

	def __repr__(self) -> str:
		return str(self.path)

	def __getitem__(self, item):
		return self.path[item]

	def __eq__(self, other):
		return self.path == other.path

	def __len__(self) -> int:
		return len(self.path)

def scx(parent1: Chromosome, parent2: Chromosome, profits: list[float]):
	p = 1   # initializing to 0 instead of 1 # STEP 1
	child = [1]

	while True:
		nodeAlfa, nodeBeta = scx_get_next_node(child, parent1, p), scx_get_next_node(child, parent2, p) # STEP 3
		print(f"Logger Inspecting Nodes : ({nodeAlfa, nodeBeta}) for child {child}")
		p = (nodeAlfa, nodeBeta)[profits[nodeAlfa-1] < profits[nodeBeta-1]]
		child.append(p)
		if child[-1] == parent1.n: # STEP 4
			return Chromosome.from_list(child)

def scx_get_next_node(child, parent, p): # STEP 2
	parent_path = parent.path.copy()
	print(p, parent_path)
	if p not in parent_path:
		parent_path = list(range(1, parent.n+1))

	ind = parent_path.index(p)
	try:
		return list(filter(lambda x: x not in child , (parent_path[ind+1:], [])[ind==len(parent_path)] ))[0]
	except IndexError:
		pass
	return list(filter(lambda x: x not in child, range(1, len(child)-1)))[0]


def mutation_add_point(child: Chromosome) -> Chromosome:
	if len(child) == child.n:
		return child

	possible_indexes = range(1, len(child)-1)

	# add random point in place of a random zero
	size = child.n
	possible_points = list(set(range(1, size + 1)) - set(child.path))

	index = random.choice(possible_indexes)
	path = child.path.copy()
	path = path[:index] + [random.choice(possible_points)] + path[index+1:]

	return Chromosome.from_list(path)


def mutation_omit_point(child: Chromosome) -> Chromosome:
	possible_indexes = [i for i, v in enumerate(child.path) if v != 0][1:-1]

	# return not mutated child if it has all zeros
	if not possible_indexes:
		return child

	size = child.n

	# change random point to a zero
	index = random.choice(possible_indexes)
	path = child.path.copy()
	path[index] = 0

	if path[1] == 1:
		print(f'omit point!')
		print(child)
		print(possible_indexes)
		print(path)

	return Chromosome.from_list(path)


def mutation_replace_point(child: Chromosome) -> Chromosome:
	possible_indexes = [i for i, v in enumerate(child.path) if v != 0][1:-1]

	# return not mutated child if it has all zeros
	if not possible_indexes:
		return child

	size = child.n
	possible_points = list(set(range(1, size + 1)) - set(child.path))

	if not possible_points:
		return child

	# change random point to a zero
	index = random.choice(possible_indexes)
	path = child.path.copy()
	path[index] = random.choice(possible_points)

	if path[1] == 1:
		print(f'replace point! {path = }')

	return Chromosome.from_list(path)

def mutation_two_opt(old_path: Chromosome, chromosome_fitness) -> Chromosome:
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
	return max(possible_new_paths, key=chromosome_fitness)

if __name__ == '__main__':
	l1 = [1, 5, 7, 3, 6, 4, 8]
	l2 = [1, 6, 2, 4, 7, 8]
	p = [1, 2, 3, 2, 3, 4, 4, 4]
	c1 = Chromosome.from_list(l1)
	c2 = Chromosome.from_list(l2)
	print(c1, c2)
	print(scx(c1, c2, p))
