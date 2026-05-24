import math
import numpy as np

four_condition = np.array([[21,5,4],[7,13,10],[2,7,21],[10,10,10]])
frontier_only = np.array([[21,5,4],[7,13,10],[10,10,10]])

def chi_square_and_cramers_v(table):
    expected = table.sum(axis=1)[:,None] * table.sum(axis=0)[None,:] / table.sum()
    chi2 = float(((table - expected) ** 2 / expected).sum())
    v = math.sqrt(chi2 / (table.sum() * min(table.shape[0]-1, table.shape[1]-1)))
    return chi2, v, expected

for name, table in [("four_condition_aggregated", four_condition), ("frontier_only_aggregated", frontier_only)]:
    chi2, v, expected = chi_square_and_cramers_v(table)
    print(f"{name}: chi-square={chi2:.6f}, Cramer's V={v:.6f}")
    print(expected)
