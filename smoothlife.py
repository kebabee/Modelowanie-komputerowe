"""
Automat komórkowy składa się z 10000 komórek w formacie 100 na 100. 
Mechanizm aktualizacji:
    1. Jeśli suma wartości komórki i jej sąsiadów (siąsiedztwo Moore’a) jest równa 4, 6, 7, 8 lub 9 
    to komórka jest żywa (równa 1) w kolejnej epoce.
    2. Jeśli suma wartości komórki i jej sąsiadów jest równa 1, 2, 3 lub 5 
    to komórka jest martwa (równa 0) w kolejnej epoce.
Dla komórek granicznych obowiązują okresowe warunki brzegowe, w kodzie realizuję je za pomocą operatora %.
Celem zadania jest zbadanie średniej wartości i odchylenia standardowegoilość żywych komórek 
dla wielu automatów startujących w tym samym zagęszczeniu żywych komórek.
"""

import numpy as np
import matplotlib.pyplot as plt

def gen_array(size_, p_):
    array = np.random.choice([0,1], size=(size_,size_), p=[1-p_,p_])
    return np.array(array)

def neighbors_count(array, i, j, size_):
    count = 0
    for x_range in range(-1, 2):
        for y_range in range(-1, 2):
            x_neighbor = (i + x_range) % size_
            y_neighbor = (j + y_range) % size_
            count += array[x_neighbor][y_neighbor]
            if count == 6:
                return count
    return count

def epoch(array1, array2, size_):
    density.append(np.sum(array2) / size / size)
    for i in range(size_):
        for j in range(size_):
            neighbors_sum = neighbors_count(array1, i, j, size_)
            if neighbors_sum in [4, 6, 7]:
                array2[i][j] = 1
            else:
                array2[i][j] = 0
    np.copyto(array1, array2)

size = 100
iters = 100
t = np.linspace(0, iters, iters+1)
results = []

for i in range(10):
    array1 = gen_array(size, 0.5)
    array2 = np.copy(array1)
    density = []
    for j in range(iters+1):
        epoch(array1, array2, size)
    plt.plot(t, density, color='b')
    results.append(density[iters-1])

print(f"Max: {max(results):.3f}")
print(f"Min: {min(results):.3f}")
print(f"Średnia: {np.mean(results):.3f}")
print(f"Odchylenie std: {np.std(results):.3f}")

plt.title("Wykres przeżywalności komórek")
plt.xlabel("Epoka automatu komórkowego")
plt.ylabel("Gęstość żywych komórek")
plt.ylim(0, 1)
plt.show()
