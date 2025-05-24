import random
import math
from common import generate_songs, generate_intervals

def ga_generate_individual(songs, target_duration, used_songs):
    min_k = math.ceil(target_duration / 180)
    max_k = math.floor(target_duration / 120)
    k = random.randint(min_k, max_k) if min_k <= max_k else min_k
    available = list(set(range(len(songs))) - set(used_songs))
    return random.sample(available, k) if k <= len(available) else []


def ga_fitness(solution, songs, target):
    total = sum(songs[i] for i in solution)
    if target - total == 0:
        return 2000 - len(solution)
    
    elif target - total == 1:
        return 1000 - len(solution)
    
    else:
        return -abs(total - target)


def selection(population, songs, target, pop_size, tournament_size=10):
     # tournoment select
    selected_population = []
    for _ in range(pop_size):
        candidates = random.sample(population, tournament_size)
        winner = max(candidates, key=lambda x: ga_fitness(x, songs, target))
        selected_population.append(winner.copy())
    return selected_population


def crossover(p1, p2):
    cross_point = random.randint(1, min(len(p1), len(p2)))
    child1 = list(set(p1[:cross_point] + p2[cross_point:]))
    child2 = list(set(p2[:cross_point] + p1[cross_point:]))
    return child1, child2

def mutate(child, songs, used_songs, mutation_rate):
    if random.random() < mutation_rate:
        if random.choice([True, False]): # 1/2 chance remove and chance 1/2 add
            child.pop(random.randint(0, len(child)-1))
        else:
            available = list(set(range(len(songs))) - set(used_songs) - set(child))
            if available:
                choice = random.choice(available) 
                child.append(choice)

    return child

def crossover_and_mutation(population, songs, used_songs, mutation_rate=0.02):
    new_population = []
    pop_size = len(population)
    for i in range(0, pop_size, 2):
        p1 = population[i]
        p2 = population[i+1]
        
        child1, child2 = crossover(p1, p2)
        
        child1 = mutate(child1, songs, used_songs, mutation_rate)
        child2 = mutate(child2, songs, used_songs, mutation_rate)
        
        new_population.append(child1)
        new_population.append(child2)
    
    return new_population

def genetic_algorithm(songs, target, used_songs, pop_size=100, generations=500):
    population = [ga_generate_individual(songs, target, used_songs) for _ in range(pop_size)]
    best_solution = []
    best_fitness = -float('inf')
    
    for _ in range(generations):
        valid_population = []
        fitnesses = []
        for ind in population:
            total = sum(songs[i] for i in ind)
            if total <= target:
                valid_population.append(ind)
                fitnesses.append(ga_fitness(ind, songs, target))

        if valid_population:
            best_idx = fitnesses.index(max(fitnesses))
            current_best = fitnesses[best_idx]
            if current_best > best_fitness:
                best_solution = valid_population[best_idx]
                best_fitness = current_best
        
        selected = selection(valid_population, songs, target, pop_size, tournament_size=3)
        population = crossover_and_mutation(selected, songs, used_songs, mutation_rate=0.1)
    return best_solution

def run_ga():
    print("=== Running Genetic Algorithm ===")
    songs = generate_songs()
    intervals = generate_intervals()
    
    print("Songs (Seconds):")
    for idx, duration in enumerate(songs):
        print(f"Song {idx}: {duration} seconds")
    
    print("\nAd Intervals (Seconds):")
    print(intervals)
    print()
    
    used_songs = set()
    for interval in intervals:
        print(f"--- Ad Interval: {interval} seconds ---")
        solution = genetic_algorithm(songs, interval, used_songs)
        selected = [(i, songs[i]) for i in solution]
        used_songs.update(solution)
        print("Genetic Algorithm Solution:")
        print(f"  Songs: {selected}")
        print(f"  Total Duration: {sum(songs[i] for i in solution)} seconds\n")

if __name__ == "__main__":
    run_ga()
