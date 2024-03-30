"""
Napisz program, który modeluje grę w Monopol, jako losowy ruch jednowymiarowy w tablicy cyklicznej 40 elementów.
Załóż, że jest jeden gracz, który rzuca dwiema kostkami i przesuwa się o wyrzuconą sumę oczek.
Zbadaj jaki jest rozkład p(i) prawdopodobieństwa p obsadzenia i-tego pola gry dla 1000 oraz 1000000 
rzutów kostkami w dwóch przypadkach:
1. Ruchu po planszy
2. Ruchu po planszy z uwzględnieniem pola 30 “idziesz do więzienia”, które przesuwa gracza na pole 10.
Wyniki przedstaw w formie wykresów p(i).
"""

import random as rd
import numpy as np
import matplotlib.pyplot as plt

def monopoly(N, prisonFlag, axis):
    p = 0
    board = np.zeros(40)
    for _ in range(N):
        p += (rd.randint(1,6) + rd.randint(1,6))
        if p >= 40:
            p -= 40
        if prisonFlag:
            if p == 29:
                p = 9
        board[p] += 1/N
    axs[axis].plot(np.linspace(1,40,40), board,'o',label=f'{N} rzutów')
    

fig, axs = plt.subplots(1, 2, figsize=(10, 5)) 

monopoly(1000, False, 0)
monopoly(1000000, False, 0)
monopoly(1000, True, 1)
monopoly(1000000, True, 1)

axs[0].set_ylim(0,0.08)
axs[0].legend()
axs[0].set_title('Rozkład p(i) bez więzienia')
axs[0].set_xlabel('numer pola')
axs[0].set_ylabel('prawdopodobieństwo')

axs[1].set_ylim(0,0.08)
axs[1].legend()
axs[1].set_title('Rozkład p(i) z więzieniem')
axs[1].set_xlabel('numer pola')
axs[1].set_ylabel('prawdopodobieństwo')

plt.tight_layout()
plt.show()
