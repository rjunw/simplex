"""
Simplex Algorithm Test Cases

Author: Ryan Wang
"""
import simplex 
import numpy as np

if __name__ == "__main__":
    # https://personal.utdallas.edu/~scniu/OPRE-6201/documents/LP06-Simplex-Tableau.pdf
    c = np.array([4, 3])
    A = np.array([
        [2, 3],
        [-3, 2],
        [0, 2],
        [2, 1]
    ])
    b = np.array([6, 3, 5, 4])
    T = simplex.make_tableau(c, A, b)
    x, T = simplex.optimize(T, return_tableau = True)
    print(T)
    print(x)
