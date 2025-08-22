import os
import numpy as np
import random

def random_walk_addition():
    cumulative_sum = 0
    while True:
        if random.random() < 0.4:
            break
        cumulative_sum += 1
    return cumulative_sum

def gerar_instancia_poisson_inteira(n, pasta_destino, lambda_poisson=5, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    
    base_elements = list(range(1, n + 1))
    subsets = []

    for _ in range(n):
        size = max(1, np.random.poisson(lambda_poisson))
        size = min(size, n)
        subset = random.sample(base_elements, size)
        subsets.append(subset)

    
    cobertura = set(e for s in subsets for e in s)
    faltantes = set(base_elements) - cobertura
    for elem in faltantes:
        i = random.randint(0, n - 1)
        subsets[i].append(elem)

    
    A = np.zeros((n, n), dtype=int)

    for i in range(n):
        for j in range(i, n):
            if (i + j) % 2 == 0:
                A[i, j] = np.random.poisson(5) + random_walk_addition()
            else:
                A[i, j] = random.randint(-10, 10) + random_walk_addition()

    
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    filepath = os.path.join(pasta_destino, f"dataset2_n{n}.txt")
    with open(filepath, 'w') as f:
        f.write(f"{n}\n")
        f.write(' '.join(str(len(s)) for s in subsets) + '\n')
        for s in subsets:
            f.write(' '.join(str(e) for e in s) + '\n')
        for i in range(n):
            f.write(' '.join(str(A[i][j]) for j in range(i, n)) + '\n')

    print(f"Instância gerada: {filepath}")

if __name__ == "__main__":
    pasta = "data"
    for n in [25, 50, 100, 200, 400]:
        gerar_instancia_poisson_inteira(n, pasta_destino=pasta)
