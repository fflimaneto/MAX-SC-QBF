#Dataset 3

import numpy as np
import random

def create_instance(n: int) -> str:

    set_matrix = np.random.rand(n, n)

    cut = 10/n
    set_matrix = np.vectorize(lambda x: 1 if x<= cut else 0)(set_matrix)

    set_dict = {}
    set_lenghts = []
    for i, row in enumerate(set_matrix):
        i += 1
        set_dict[i] = []
        for variable, value in enumerate(row):
            if value:
                set_dict[i].append(str(variable + 1))

        if str(i) not in set_dict[i]:
            set_dict[i].append(str(i))

        set_lenghts.append(str(len(set_dict[i])))

    instance = [f'{n}']

    instance += [' '.join(set_lenghts)]

    for i, variables in set_dict.items():
        instance += [' '.join(variables)]

    value_matrix = -5 + np.random.randn(n, n) * 15

    value_matrix = np.vectorize(lambda x: int(x))(value_matrix)

    for i, row in enumerate(value_matrix):
        values = list(map(str, row[i:len(row)]))
        instance += [' '.join(values)]

    return '\n'.join(instance)

set_sizes = [25,50,100,200,400]

for size in set_sizes:

    instance = create_instance(size)

    file_name = f"dataset3_n{size}.txt"

    with open(file_name, "w") as file:
        file.write(instance)


