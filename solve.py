import os
import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import csv

def ler_instancia(filepath):
    with open(filepath, 'r') as f:
        lines = f.read().strip().split('\n')

    idx = 0
    n = int(lines[idx])
    idx += 1

    sizes = list(map(int, lines[idx].split()))
    idx += 1

    subsets = []
    for s in sizes:
        subset = list(map(int, lines[idx].split()))
        subsets.append([e - 1 for e in subset])  # ajusta para zero-based
        idx += 1

    A = np.zeros((n, n))
    for i in range(n):
        values = list(map(float, lines[idx].split()))
        for j, val in enumerate(values):
            A[i][i + j] = val
        idx += 1

    return n, subsets, A

def resolver_modelo(n, subsets, A, time_limit=600):
    base_elements = set(range(n))
    e = {(k, i): 1 if k in subsets[i] else 0 for k in base_elements for i in range(n)}

    model = gp.Model()
    model.Params.LogToConsole = 0
    model.Params.TimeLimit = time_limit

    x = model.addVars(n, vtype=GRB.BINARY, name="x")
    y = model.addVars(n, n, vtype=GRB.BINARY, name="y")

    obj = gp.LinExpr()
    for i in range(n):
        for j in range(i, n):
            obj.add(A[i][j] * y[i, j])
    model.setObjective(obj, GRB.MAXIMIZE)

    model.addConstrs((y[i, j] <= x[i] for i in range(n) for j in range(i, n)))
    model.addConstrs((y[i, j] <= x[j] for i in range(n) for j in range(i, n)))
    model.addConstrs((y[i, j] >= x[i] + x[j] - 1 for i in range(n) for j in range(i, n)))

    for k in base_elements:
        model.addConstr(gp.quicksum(e[k, i] * x[i] for i in range(n)) >= 1)

    model.optimize()
    exec_time = model.Runtime

    if model.Status == GRB.OPTIMAL or model.Status == GRB.TIME_LIMIT:
        pb = model.ObjVal
        db = model.ObjBound
        gap = abs((db-pb)/db) if model.MIPGap is not None else -1
        return pb, db, gap, exec_time
    else:
        return None, None, None, exec_time

def resolver_todas_instancias(instancias, arquivo_saida='results.csv', single_instance=False):

    resultados = []
    
    if single_instance:
        instancia = instancias.rsplit('\\', 1)[-1].rsplit('/', 1)[-1]
        arquivos = [instancia]
        arquivo_saida = instancia.rsplit('.', 1)[0] + '.csv'
    else:
        arquivos = [f for f in os.listdir(instancias) if f.endswith('.txt')]
        arquivos.sort()
        
        if not len(arquivos):
            print("Instance files need to be within a \'data\' directory")
            return

    for arquivo in arquivos:
        caminho = os.path.join("data", arquivo)
        print(f"Solving {arquivo}...")

        n, subsets, A = ler_instancia(caminho)
        pb, db, gap, tempo = resolver_modelo(n, subsets, A)

        resultados.append({
            "arquivo": arquivo,
            "n": n,
            "primal_bound": pb,
            "dual_bound": db,
            "gap": gap,
            "tempo": tempo
        })

    with open(arquivo_saida, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["arquivo", "n", "primal_bound", "dual_bound", "gap", "tempo"])
        writer.writeheader()
        writer.writerows(resultados)

    print(f"\nResults saved within {arquivo_saida}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        resolver_todas_instancias("data")
    else:
        resolver_todas_instancias(sys.argv[1], single_instance=True)