import numpy as np
import random
from scipy import stats

def save_to_txt(n, subsets, A,):
    name = f"dataset1_n{n}.txt"
    with open(name, 'w') as f:
        f.write(f"{n}\n")
        
        sizes = [len(subset) for subset in subsets]
        f.write(" ".join(map(str, sizes)) + "\n")
        
        for subset in subsets:
            f.write(" ".join(map(str, sorted(subset))) + "\n")
        
        for i in range(n):
            row_elements = [f"{A[i,j]:.6f}" for j in range(i, n)]
            f.write(" ".join(row_elements) + "\n")


# Just to add a little bit more randomness
def random_walk_addition():
    cumulative_sum = 0
    while True:
        if random.random() < 0.4:
            break
        cumulative_sum += 1
    
    return cumulative_sum

def generate_subsets_with_distributions(n, subsets_config, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    
    base_numbers = list(range(1, n+1))
    
    while True:
        subsets = []
        
        for i, size in enumerate(subsets_config):
            if size > n:
                print("A subset cannot be greater then the size of n") 
            
            if i % 2 == 0:
                # Normal distribution  
                mean = n/2
                std = n/4
                x = np.arange(1, n+1)
                weights = stats.norm.pdf(x, mean, std)
                weights = weights / weights.sum() 
            
            else:
                # Geometric distribution
                p = 0.5
                x = np.arange(1, n+1)
                weights = stats.geom.pmf(x, p)
                weights = weights / weights.sum()
            
            subset = np.random.choice(base_numbers, p=weights, replace=False, size=size)
            subsets.append(list(subset))
        
        union = set()
        for subset in subsets:
            union.update(subset)
        
        if union == set(base_numbers):
            break
    
    return subsets

def generate_matrix_with_distributions(n, seed=42):
    np.random.seed(seed)
    random.seed(seed)
    
    A = np.zeros((n, n), dtype=int)
    
    for i in range(n):
        for j in range(i, n):
            # poisson Distribution
            if (i + j) % 2 == 0:
                    lam =  5
                    A[i, j] = np.random.poisson(lam) + random_walk_addition()
    
            else:
                # Uniform distribution
                    low = -10
                    high =  10
                    A[i, j] = random.randint(low, high) + random_walk_addition()
  
    
    return A

def main():
    sizes = [25, 50, 100, 200, 400]
    for n in sizes:
        subsets_config = [random.randint(int(n/5), int(n/2)) for _ in range(n)]

        subsets = generate_subsets_with_distributions(n, subsets_config)
        A = generate_matrix_with_distributions(n)
        save_to_txt(n, subsets, A)

if __name__ == "__main__":
    main()