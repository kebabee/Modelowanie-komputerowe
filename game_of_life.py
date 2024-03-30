"""Gra w życie. Automat komórkowy składa się z n^2 komórek w formacie n na n.
Mechanizm aktualizacji:
    1. Martwa komórka staje się żywa w kolejnej epoce jeśli liczba żywych sąsiadów (sąsiedztwo Moore'a) wynosi 3.
    2. Żywa komórka pozostaje żywa w kolejnej epoce jeśli liczba sąsiadów wynosi 2 lub 3.
    3. W innych przypadkach komórka staje się lub pozostaje martwa.
Dla komórek granicznych obowiązują okresowe warunki brzegowe, w kodzie realizuję je za pomocą operatora \%.
Celem zadania jest implementacja modelu automatu komórkowego, analiza przeżywalności komórek w zależności od początkowej gęstości żywych komórek 
oraz analiza błędu standardowego wyznaczania średniej w zależności od rozmiaru automatu."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import sem # błąd standardowy

def neighborsCount(array, i, j): # liczenie sąsiedztwa Moore'a
    size = array.shape[0]
    count = 0
    for x_range in range(-1, 2):
        for y_range in range(-1, 2):
            if x_range == 0 and y_range == 0:
                continue
            x_neighbor = (i + x_range) % size
            y_neighbor = (j + y_range) % size
            count += array[x_neighbor][y_neighbor]
            if count == 4: # jeśli będą 4 to nie musimy sprawdzać dalej
                return count
    return count

def epoch(array1, array2): # aktualizacja stanu automatu
    size = array2.shape[0]
    density.append(np.sum(array2) / size / size) # zapis aktualnej gęstości
    for i in range(size):
        for j in range(size):
            neighbor_sum = neighborsCount(array1, i, j)
            if neighbor_sum == 3 and array2[i][j] == 0:
                array2[i][j] = 1
            elif neighbor_sum in [2,3] and array2[i][j] == 1:
                array2[i][j] = 1
            else:
                array2[i][j] = 0
    np.copyto(array1, array2)

def gen_array(size_, p_): # generator tablicy o zadanym rozmiarze i p0
    array = np.random.choice([0,1], size=(size_,size_), p=[1-p_,p_])
    return np.array(array)


# końcowa gęstośc a p0
size = 100
iters = 100
t = np.linspace(0, iters, iters+1)
p0_id = 0
p0s = [0.05, 0.1, 0.3, 0.4, 0.5, 0.6, 0.75, 0.8, 0.95]
end_densities = [[],[],[],[],[],[],[],[],[]]

fig, axs = plt.subplots(3, 3, figsize=(12, 12))
for i in range(3):
    for j in range(3):
        for _ in range(3):
            array1 = gen_array(size, p0s[p0_id])
            array2 = np.copy(array1)
            density = []
            for _ in range(iters+1):
                epoch(array1, array2)
            index = i * 3 + j
            axs[i,j].set_ylim(-0.01,0.35)
            axs[i,j].set_xlabel("epoki")
            axs[i,j].set_ylabel("gęstość żywych komórek")
            axs[i, j].plot(t, density, c='b')
            end_densities[p0_id].append(density[len(density)-1])
        axs[i, j].set_title(f'Przebieg dla p0 = {p0s[p0_id]}')
        p0_id += 1

plt.tight_layout()
plt.show()

serrs = [] # tablica błędów standardowych
means = [] # tablica średnich
print("p0\tmin\tmax\tśrednia\tbłąd stand.")
for i in range(9):
    print(f"{p0s[i]}\t{np.min(end_densities[i]):.3f}\t{np.max(end_densities[i]):.3f}\t{np.mean(end_densities[i]):.3f}\t{sem(end_densities[i]):.3f}")
    serrs.append(sem(end_densities[i]))
    means.append(np.mean(end_densities[i]))
    
plt.scatter(p0s, means)
plt.errorbar(p0s, means, yerr=serrs, fmt="o")
plt.ylabel("średnia gęstość końcowa")
plt.xlabel("gęstość początkowa")
plt.title("Zależność końcowej gęstości od p0")
plt.show()

# Błąd standardowy dla róznych rozmiarów automatów
serrs = []
end_densities = []
iters = 500
sizes = [10, 50, 100, 200, 500]

for size in sizes:
    temp = []
    array1 = gen_array(size, 0.4)
    array2 = np.copy(array1)
    for _ in range(20):
        density = []
        for _ in range(iters):
            epoch(array1, array2)
        temp.append(density[iters-1])
    end_densities.append(temp)

print("\nrozm.\tmin\tmax\tśrednia\tbłąd stand.")
for i in range(5):
    print(f"{sizes[i]}\t{np.min(end_densities[i]):.3f}\t{np.max(end_densities[i]):.3f}\t{np.mean(end_densities[i]):.3f}\t{sem(end_densities[i]):.7f}")
    serrs.append(sem(end_densities[i]))

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(sizes, serrs, 'o')
plt.title('Zmiana błędu standardowego')
plt.xlabel('rozmiar automatu')
plt.ylabel('błąd standardowy')

plt.subplot(1, 2, 2)
plt.plot(np.log(sizes), np.log(serrs), 'o')
plt.title('Zmiana błedu standardowego (log-log)')
plt.xlabel('rozmiar automatu (log)')
plt.ylabel('błąd standardowy (log)')

plt.tight_layout()
plt.show()
