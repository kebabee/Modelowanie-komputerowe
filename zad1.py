import random as rd
import numpy as np
import matplotlib.pyplot as plt

def monopoly(N, prisonFlag=False):
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
    plt.plot(t,board,'o',label=f'{N} rzutów')
    
    
t = np.linspace(1,40,40)

monopoly(100)
monopoly(1000000)
plt.ylim(0,0.08)
plt.legend()
plt.title('Rozkład prawdopodobieństwa trafienia na pole, bez więzienia')
plt.xlabel('numer pola')
plt.ylabel('prawdopodobieństwo')
plt.show()

monopoly(1000000, True)
plt.ylim(0,0.055)
plt.legend()
plt.title('Rozkład prawdopodobieństwa trafienia na pole, z więzieniem')
plt.xlabel('numer pola')
plt.ylabel('prawdopodobieństwo')
plt.show()