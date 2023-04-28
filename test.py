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
    x, T = simplex.optimize(T, return_tableau = True, verbose = True)
    print(x)

    # https://jeremykun.com/2014/12/01/linear-programming-and-the-simplex-algorithm/
    c = np.array([3, 2])
    A = np.array([
        [1, 2],
        [1, -1],
    ])
    b = np.array([4, 1])
    T = simplex.make_tableau(c, A, b)
    x, T = simplex.optimize(T, return_tableau = True, verbose = True)
    print(x)

    # https://math.mit.edu/~goemans/18310S15/lpnotes310.pdf
    c = np.array([20, 16, 12])
    A = np.array([
        [1, 0, 0],
        [2, 1, 1],
        [2, 2, 1],
    ])
    b = np.array([4, 10, 16])
    T = simplex.make_tableau(c, A, b)
    x, T = simplex.optimize(T, return_tableau = True, verbose = True)
    print(x)