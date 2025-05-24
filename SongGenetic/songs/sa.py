import random
import math
from common import generate_songs, generate_intervals

def sa_energy(solution, songs, target):

    total = sum(songs[i] for i in solution)
    
    if total > target:
        return float('inf')  

    return (target - total) * 100 + len(solution)

def generate_initial_solution(songs, used_songs, target):
    available = list(set(range(len(songs))) - set(used_songs))
    random.shuffle(available)
    
    solution = []
    total = 0

    for song in available:
        if total + songs[song] <= target:
            solution.append(song)
            total += songs[song]

    return solution

def generate_neighbor(solution, songs, used_songs, target):
    available = list(set(range(len(songs))) - set(used_songs))
    neighbor = solution.copy()
    total = sum(songs[i] for i in neighbor)

    action = random.choice(['add', 'remove', 'replace'])

    if action == 'add' and len(available) > 0:
        new_song = random.choice(list(set(available) - set(neighbor)))
        if total + songs[new_song] <= target:  # Ensure adding keeps duration under target
            neighbor.append(new_song)

    elif action == 'remove' and len(neighbor) > 1:
        neighbor.pop(random.randint(0, len(neighbor) - 1))

    elif action == 'replace' and len(neighbor) > 0:
        replace_idx = random.randint(0, len(neighbor) - 1)
        new_song = random.choice(list(set(available) - set(neighbor)))
        if total - songs[neighbor[replace_idx]] + songs[new_song] <= target:
            neighbor[replace_idx] = new_song

    return neighbor

def simulated_annealing(songs, target, used_songs, temp=10000, cooling=0.95):
    current = generate_initial_solution(songs, used_songs, target)
    best = current.copy()
    current_e = sa_energy(current, songs, target)
    best_e = current_e

    while temp > 0.1:
        neighbor = generate_neighbor(current, songs, used_songs, target)
        neighbor_e = sa_energy(neighbor, songs, target)

        if neighbor_e < current_e or random.random() < math.exp((current_e - neighbor_e) / temp):
            current = neighbor
            current_e = neighbor_e

        if neighbor_e < best_e:
            best = neighbor.copy()
            best_e = neighbor_e

        temp *= cooling

    total = sum(songs[i] for i in best)
    return best

def run_sa():
    print("=== Running Simulated Annealing (Strictly Under Target) ===")
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
        solution = simulated_annealing(songs, interval, used_songs)
        if solution:
            selected = [(i, songs[i]) for i in solution]
            used_songs.update(solution)
            print("Simulated Annealing Solution:")
            print(f"  Songs: {selected}")
            print(f"  Total Duration: {sum(songs[i] for i in solution)} seconds\n")

if __name__ == "__main__":
    run_sa()
 