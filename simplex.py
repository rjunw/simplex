"""
Simplex Algorithm

Author: Ryan Wang
"""

import numpy as np 

def make_tableau(c, A, b, obj_const = 0):
    """
    Given canonical c = (c1, ..., cn), and constraints A in mxn, b = (b1, ..., bm):
        maximize     z = c^Tx 
        subject to   Ax <= b
        where        x >= 0
    Return (m + 1) x (n + m + 2) augmented matrix (simplex tableau) representation
    """
    n = c.shape[0] # non-basic variables
    m = A.shape[0] # basic variables

    # Tableau will have rows m constraints + objective => m + 1
    # Tableau will have 1 z + n + m variables + column b => n + m + 1 columns
    T = np.zeros((m + 1, n + m + 2))

    # set objective to first row
    c_slack = np.concatenate([np.array([1]), -c])
    T[0, :n + 1] = c_slack 

    # constraint coefficients + slack coefficients
    T[1:m + 1, 1:n + m + 1] = np.concatenate([A, np.eye(m)], axis = 1) 

    # constraint constant
    T[1:m+1, n + m + 1] = b
    T[0, n+m+1] = obj_const

    return T

def dv0_coalesce(a, b, how = np.inf):
    return np.divide(a, b, 
                     out=np.ones_like(a) * how, 
                     where=~np.isclose(b,np.zeros_like(b)))

def pivot(T):
    """
    Perform one pivot operation on a simplex tableau

    Return pivot cell and new pivoted tableau
    """
    # pivot column will be most negative => direction of most increase
    pivot_col = np.argmin(T[0, 1:]) + 1
    
    # pivot row requires min ratio test => maximize increase in column var
    coefs = T[1:, pivot_col].copy()
    rhs = T[1:, -1].copy()
    coefs[coefs <= 0] = 0 # only take into account non-positive coefficients
    ratios = dv0_coalesce(rhs, coefs, how = np.inf)
    pivot_row = np.argmin(ratios) + 1

    # by pivoting, pivot col variable 'enters', pivot_row slack 'leaves'
    T_pivot = T.copy()
    pivot_val = T_pivot[pivot_row, pivot_col]
    T_pivot[pivot_row, :] = T_pivot[pivot_row, :]/pivot_val

    for row_idx in range(T_pivot.shape[0]):
        if row_idx != pivot_row:
            # Gaussian Elimination
            scale = T_pivot[row_idx, pivot_col]
            T_pivot[row_idx, :] = T_pivot[row_idx, :] + (-scale) * T_pivot[pivot_row, :]

    return T_pivot 

def is_optimal(T):
    """
    If coefficients of first row are all positive, optimal solution
    """
    return (T[0, 1:] >= 0).all()

def optimize(T, return_tableau = False, verbose = False):
    """
    Optimize the linear programming problem given by augmented 
    simplex matrix

        [1  -c   0 | 0]
        [0   A   I | b]

    Returns final solution (x) and final tableau
    """
    m = T.shape[0] - 1
    n = T.shape[1] - m - 2

    # initial BFS (x1 = 0, ..., xn = 0, s1 = b1, ... sn = bn)
    x = T[:, n + m + 1] 

    # Simplex algorithm
    i = 0
    while not is_optimal(T): 
        if verbose:
            print(f"Tableau {i}: \n{T}")
        T = pivot(T)
        x = T[:, n + m + 1] 
        i += 1
        
    if verbose:
        print(f"Tableau {i}: \n{T}")
    # get isolated non-basic variables
    mask = np.count_nonzero(T[1:, 1:n+1], axis = 1)
    mask = mask == 1
    sol = []
    for col_idx in range(mask.shape[0]):
        if mask[col_idx]:
            if T[1:, col_idx + 1].sum() == 1:
                sol.append(x[col_idx])
        else:
            sol.append(0)

    if return_tableau:
        return sol, T 
    else:
        return sol