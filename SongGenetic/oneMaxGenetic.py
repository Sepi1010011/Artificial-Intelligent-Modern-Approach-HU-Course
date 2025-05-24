import random
#Help taken from GeeksforGeeks and chatgpt
#parametrs:
populationSize = 50
genomeLength = 20
mutationRate = 0.02
crossoverRate = 0.7
generations = 300

#make genome
def create_individual():
    return [random.randint(0, 1) for i in range(genomeLength)]

#make population
def initializePopulations():
    return [create_individual() for i in range(populationSize)]

#fitness function
def fitness(individual):
    return sum(individual)

#selection function used roulette wheel
def roulette_select_individual(population, probabilities):
    random_point = random.uniform(0, 1)
    cumulative_probability = 0
    for individual, probability in zip(population, probabilities):
        cumulative_probability += probability
        if random_point <= cumulative_probability:
            return individual


def roulette_Wheel_selection(population, fitnessValues, n_pair):
    total_fitness = sum(fitnessValues)
    probabilities = [x / total_fitness for x in fitnessValues]
    selected = []
    for i in range(n_pair):
        x1 = roulette_select_individual(population, probabilities)
        x2 = roulette_select_individual(population, probabilities)
        selected.append(x1)
        while x2 == x1:
            x2 = roulette_select_individual(population, probabilities)
        selected.append(x2)
    return selected

#mutate function
def mutate(individual):
    if random.random() < mutationRate:
        i = random.randint(0, genomeLength-1)
        individual[i] = 1 - individual[i]

#single point crossover
def crossover(parent1, parent2):
    if random.random() < crossoverRate:
        crossover_point = random.randint(1, genomeLength - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
    else:
        child1, child2 = parent1, parent2
    return child1, child2

# genetic algorithm for 300 generation
def evolve():
    population = initializePopulations()

    for generation in range(generations):
        fitnessValues = [fitness(ind) for ind in population]

        best_individual = max(population, key=fitness)
        best_fitness = fitness(best_individual)
        print(f"Generation {generation}: Best fitness = {best_fitness}, Best individual = {best_individual}")

        if best_fitness == genomeLength:
            print(f"Solution found in generation {generation}")
            break

        parents = roulette_Wheel_selection(population, fitnessValues, populationSize // 2)

        next_generation = []
        for i in range(0, len(parents), 2):
            child1, child2 = crossover(parents[i], parents[i+1])
            mutate(child1)
            mutate(child2)
            next_generation.extend([child1, child2])
        population = next_generation

    final_best_individual = max(population, key=fitness)
    print("\nFinal Best Individual:", final_best_individual)
    print("Final Best Fitness:", fitness(final_best_individual))

evolve()