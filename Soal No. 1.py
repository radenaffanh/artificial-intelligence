import random

# Parameter
POP_SIZE = 4
CHROM_LENGTH = 5
GENERATIONS = 10
MUTATION_RATE = 0.1

# Fitness function
def fitness(x):
    return x**2

# Generate random chromosome
def random_chromosome():
    return ''.join(random.choice('01') for _ in range(CHROM_LENGTH))

# Convert binary to decimal
def decode(chrom):
    return int(chrom, 2)

# Roulette wheel selection
def selection(population, fitnesses):
    total_fit = sum(fitnesses)

    probs = [f / total_fit for f in fitnesses]

    cumulative = []
    current = 0

    for p in probs:
        current += p
        cumulative.append(current)

    selected = []

    for _ in range(len(population)):
        r = random.random()

        for i, c in enumerate(cumulative):
            if r <= c:
                selected.append(population[i])
                break

    return selected

# 1-point crossover
def crossover(parent1, parent2):
    point = random.randint(1, CHROM_LENGTH - 1)

    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    return child1, child2

# Mutation
def mutate(chromosome):
    chrom = list(chromosome)

    for i in range(CHROM_LENGTH):
        if random.random() < MUTATION_RATE:
            chrom[i] = '1' if chrom[i] == '0' else '0'

    return ''.join(chrom)

# Initial population
population = [random_chromosome() for _ in range(POP_SIZE)]

print("Populasi Awal:")
print(population)

best_individual = None
best_fitness = -1

# Evolution process
for gen in range(GENERATIONS):

    # Decode and evaluate
    decoded = [decode(ch) for ch in population]
    fitnesses = [fitness(x) for x in decoded]

    # Individu Terbaik
    max_fit = max(fitnesses)
    idx = fitnesses.index(max_fit)

    if max_fit > best_fitness:
        best_fitness = max_fit
        best_individual = population[idx]

    print(f"\nGenerasi {gen+1}")
    print("Populasi:", population)
    print("Fitness:", fitnesses)
    print("Best:", population[idx],
          "x =", decoded[idx],
          "fitness =", max_fit)

    # Selection
    selected = selection(population, fitnesses)

    # Crossover
    new_population = []

    for i in range(0, POP_SIZE, 2):
        p1 = selected[i]
        p2 = selected[i+1]

        c1, c2 = crossover(p1, p2)

        new_population.extend([c1, c2])

    # Mutation
    population = [mutate(ch) for ch in new_population]

# Final result
print("\nHASIL AKHIR")
print("Individu terbaik:", best_individual)
print("Nilai x:", decode(best_individual))
print("Fitness terbaik:", best_fitness)