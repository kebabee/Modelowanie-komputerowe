"""
Prawo Zipfa to prawo empiryczne, które często obowiązuje w przybliżeniu, gdy lista mierzonych wartości jest posortowana w porządku malejącym. 
Stwierdza ono, że wartość n-tego elementu jest odwrotnie proporcjonalna do n. 
Najbardziej znany przykład prawa Zipfa odnosi się do tabeli częstotliwości słów w tekście lub korpusie języka naturalnego:*
    częstotliwość występowania słowa ~ 1 \ ranking słowa
Celem zadania jest opracowanie programu badającego prawo Zipfa w dostarczonych plikach tekstowych.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def zipfs_law(text):
    # usuwanie kropek, przecinków itp + wszystko z małej litery
    marks = [',','.','[',']','-','—','…','!','?',':',';','(',')']
    for mark in marks:
        text = text.replace(mark,'')
    text = text.lower()
    words = text.split()
    print(f"Liczba słów w tekście: {len(words)}")
    zipf_dict = {}
    for word in words:
        if word in zipf_dict.keys():
            zipf_dict[word] += 1
        else:
            zipf_dict[word] = 1
    zipf_dict = {k: v for k, v in sorted(zipf_dict.items(), key=lambda item: item[1], reverse=True)} # sortowanie malejąco po value
    values = list(zipf_dict.values())
    keys = list(zipf_dict.keys())
    ranks = np.linspace(1,len(keys),len(keys))
    densities = [a/len(words) for a in values] # częstotliwość występowania słowa w tekście
    return ranks, densities, values, keys


print("Artykuł 'Big Bang' z wikipedii:")
with open('wikipedia.txt', 'r') as file:
    wikipedia_txt = file.read()
wikipedia_ranks, wikipedia_densities, wikipedia_values, wikipedia_keys = zipfs_law(wikipedia_txt)
print("Najrzadsze:")
print(wikipedia_keys[-10:])
print("Najczestsze:")
print(wikipedia_keys[:10])

print("Sprawozdanie stenograficzne z posiedzenia sejmu:")
with open('sejm.txt', 'r') as file:
    sejm_txt = file.read()
sejm_ranks, sejm_densities, sejm_values, sejm_keys = zipfs_law(sejm_txt)
print("Najrzadsze:")
print(sejm_keys[-10:])
print("Najczestsze:")
print(sejm_keys[:10])

print("Kompilacja 10 przepisów na pierogi ruskie")
with open('pierogi.txt', 'r') as file:
    pierogi_txt = file.read()
pierogi_ranks, pierogi_densities, pierogi_values, pierogi_keys = zipfs_law(pierogi_txt)
print("Najrzadsze:")
print(pierogi_keys[-10:])
print("Najczęstsze:")
print(pierogi_keys[:10])

plt.plot(np.log(sejm_ranks), np.log(sejm_densities),'o',label='sejm')
plt.plot(np.log(wikipedia_ranks), np.log(wikipedia_densities),'o',label='Big Bang')
plt.plot(np.log(pierogi_ranks), np.log(pierogi_densities),'o',label='przepisy')
plt.xlabel("log(ranking słowa)")
plt.ylabel("log(częstotliwośc wystąpień słowa)")
plt.title("Rozkład wystąpień słów (log-log) - trzy przypadki")
plt.legend()
plt.show()

# fitowanie
def f2(x, c, b):
    return c * x ** b

fit_densities = sejm_densities[8:477]
fit_densities_1 = wikipedia_densities[7:390]
fit_densities_2 = pierogi_densities[7:168]

sejm_popt, pcov = curve_fit(f2, np.linspace(9, len(fit_densities) + 8, len(fit_densities)), fit_densities)
wikipedia_popt, pcov = curve_fit(f2, np.linspace(9, len(fit_densities_1) + 8, len(fit_densities_1)), fit_densities_1)
pierogi_popt, pcov = curve_fit(f2, np.linspace(9, len(fit_densities_2) + 8, len(fit_densities_2)), fit_densities_2)

print("Parametry dla sprawozdania stenograficznego:")
print(f"c = {sejm_popt[0]:.3f}")
print(f"b = {sejm_popt[1]:.3f}\n")
print("Parametry dla artykułu 'Big Bang':")
print(f"c = {wikipedia_popt[0]:.3f}")
print(f"b = {wikipedia_popt[1]:.3f}\n")
print("Parametry dla przepisów na pierogi:")
print(f"c = {pierogi_popt[0]:.3f}")
print(f"b = {pierogi_popt[1]:.3f}\n")

fig, axs = plt.subplots(1, 3, figsize=(15, 5))

axs[1].plot(np.log(sejm_ranks), np.log(sejm_densities), 'o', label='rozkład')
axs[1].plot(np.log(np.linspace(9, len(fit_densities) + 8, len(fit_densities))), np.log(fit_densities), 'o', label='fitowany tekst')
axs[1].plot(np.log(sejm_ranks), np.log(f2(sejm_ranks,sejm_popt[0],sejm_popt[1])), label=f'{sejm_popt[0]:.2f}r^{sejm_popt[1]:.2f}')
axs[1].legend()
axs[1].set_xlabel("log(ranking słowa)")
axs[1].set_ylabel("log(częstotliwośc wystąpień słowa)")
axs[1].set_title("sprawozdanie stenograficzne")
axs[1].set_ylim(-10,-2)

axs[0].plot(np.log(wikipedia_ranks), np.log(wikipedia_densities), 'o', label='rozkład')
axs[0].plot(np.log(np.linspace(8, len(fit_densities_1) + 7, len(fit_densities_1))), np.log(fit_densities_1), 'o', label='fitowany tekst')
axs[0].plot(np.log(wikipedia_ranks), np.log(f2(wikipedia_ranks,wikipedia_popt[0],wikipedia_popt[1])), label=f'{wikipedia_popt[0]:.2f}r^{wikipedia_popt[1]:.2f}')
axs[0].legend()
axs[0].set_xlabel("log(ranking słowa)")
axs[0].set_ylabel("log(częstotliwośc wystąpień słowa)")
axs[0].set_title("Big Bang")
axs[0].set_ylim(-10,-2)

axs[2].plot(np.log(pierogi_ranks), np.log(pierogi_densities), 'o', label='rozkład')
axs[2].plot(np.log(np.linspace(8, len(fit_densities_2) + 7, len(fit_densities_2))), np.log(fit_densities_2), 'o', label='fitowany tekst')
axs[2].plot(np.log(pierogi_ranks), np.log(f2(pierogi_ranks,pierogi_popt[0],pierogi_popt[1])), label=f'{pierogi_popt[0]:.2f}r^{pierogi_popt[1]:.2f}')
axs[2].legend()
axs[2].set_xlabel("log(ranking słowa)")
axs[2].set_ylabel("log(częstotliwośc wystąpień słowa)")
axs[2].set_title("przepisy")
axs[2].set_ylim(-10,-2)

plt.tight_layout()
plt.show()
