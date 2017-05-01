import numpy as np
import sympy as sp


class StiffnessMatrix:
    STIFFNESS_MATRIX = """np.mat([[12*E*I/L**3, 6*E*I/L**2, -12*E*I/L**3, 6*E*I/L**2],
                               [6*E*I/L**2, 4*E*I/L, -6*E*I/L**2, 2*E*I/L],
                               [-12*E*I/L**3, -6*E*I/L**2, 12*E*I/L**3, -6*E*I/L**2],
                               [6*E*I/L**2, 2*E*I/L, -6*E*I/L**2, 4*E*I/L]])"""

    def __init__(self, E, I, L):
        self.stiffnessMatrix = eval(self.STIFFNESS_MATRIX)

