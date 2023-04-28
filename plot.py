"""
Simplex Algorithm Plotting Methods

Author: Ryan Wang
"""
import numpy as np
import matplotlib.pyplot as plt
import time
import simplex

def plot_feasible(c, A, b, size = 30, detail = 100):
    """
    Plot the 2-D feasible region given constraint matrix A and contraint constant b

        size -- width/height of plot
        detail -- number of linspace splits
    """
    x1, x2 = np.meshgrid(np.linspace(0, size, detail), np.linspace(0, size, detail))

    ### 1. compute objective over grid
    z = c[0] * x1 + c[1] * x2

    ### 2. var constraints over entire grid
    mask = np.ones_like(z)
    for row_idx in range(detail):
        for col_idx in range(detail):
            x1_constraints = A[:, 0] * x1[row_idx, col_idx] 
            x2_constraints = A[:, 1] * x2[row_idx, col_idx]

            if (x1_constraints + x2_constraints > b).any():
                mask[row_idx, col_idx] = 0

    ### 3. mask out out of constraint points
    z_constrained = z * mask
    print(f"Maximum Objective: {z_constrained.max()}")
    plt.contourf(x1, x2, z_constrained, levels = np.arange(z_constrained.min(), z_constrained.max(), 0.1)) 
    plt.colorbar()
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.title('Feasible region defined by Ax <= b')

def plot_vertex(T):
    """
    Given Tableau, plot the vertex of the feasible region we are in
    """
    m = T.shape[0] - 1
    n = T.shape[1] - 2 - m

    # 1. get x's
    x = T[:, n + m + 1] 


    # 2. get corresponding b (as per simplex.py)
    ### look for non-zero columns with one non-zero value
    mask = np.count_nonzero(T[1:, 1:n+1], axis = 0) 
    mask = mask == 1

    ### build solution by solving for single variables
    sol = []
    for col_idx in range(mask.shape[0]):
        if mask[col_idx]: 
            piv_index = np.argmax(T[1:, col_idx + 1])
            sol.append(x[piv_index + 1]/T[piv_index + 1, col_idx + 1])
        else:
            sol.append(0)
    print(f"Current Objective: {T[0, -1]}")
    plt.scatter(sol[0], sol[1], c='r', marker = 'D', s= 50, clip_on = False)

def animate(c, A, b, obj_const = 0, size=30, detail=100, reset_frames = False, verbose = False):
    """
    reset_frames doesn't really work...
    """
    # initial BFS
    plot_feasible(c, A, b, size, detail)
    T = simplex.make_tableau(c, A, b, obj_const)
    if verbose: print(f"Initial Tableau: \n{T}")
    plot_vertex(T)
    if reset_frames: plt.show();time.sleep(1)
    i = 0
    while not simplex.is_optimal(T):
        T = simplex.pivot(T)
        plot_feasible(c, A, b, size, detail)
        if verbose: print(f"Tableau {i + 1}: \n{T}")
        i += 1
        plot_vertex(T)
        if reset_frames: plt.show();time.sleep(1)

