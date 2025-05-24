from ga import run_ga
from sa import run_sa

def main():
    print("=== Genetic Algorithm Execution ===")
    run_ga()
    
    print("\n" + "=" * 50 + "\n")
    
    print("=== Simulated Annealing Execution ===")
    run_sa()

if __name__ == "__main__":
    main()
