from SimulatingScaleFreePercolation import SimulatingScaleFreePercolation, Vertex
from Distribution import Distribution
from scipy import stats
import numpy as np

'''
Inherits SimulatingScaleFreePercolation, works mostly the same but the locations are off the grid. 

https://stackoverflow.com/a/31202320 method to generate for poisson point process.
'''
class SimulatingPoissonAlternative(SimulatingScaleFreePercolation):

    def __init__(self):
        super().__init__()

    #Override
    def setVertices(self, w, h):
        n = np.random.poisson(w*h)
        x = np.random.rand(n)*w
        y = np.random.rand(n)*h 
        self.vertices = []
        id = 0
        for (i, j) in zip(x, y):
            self.vertices.append(Vertex(id, i, j))
            id += 1