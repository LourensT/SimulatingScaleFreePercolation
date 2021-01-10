import os
from SimulatingScaleFreePercolation import SimulatingScaleFreePercolation
from SimulatingPoissonAlternative import SimulatingPoissonAlternative

style = ["\SetVertexStyle[MinSize=0.1\DefaultUnit, LineWidth=0pt, FillColor=mycolor1]\n", "\SetEdgeStyle[LineWidth=0.25pt]\n"]

#Scale Free Percolation
sim = SimulatingScaleFreePercolation()
sim.generateGraph(25, 25, 0.625, 2.5, 3)
sim.draw(fp="tau2,5.tikz", style=style)
sim.saveDegreeDistribution("tau2,5_degreedistr.tikz")
sim.generateGraph(25, 25, 0.625, 3.5, 3)
sim.draw(fp="tau3,5.tikz", style=style)
sim.saveDegreeDistribution("tau3,5_degreedistr.tikz")

#Poisson Alternative (instead of Grid)
sim = SimulatingPoissonAlternative()
sim.generateGraph(25, 25, 0.625, 2.5, 3)
sim.draw(fp="poi_tau2,5.tikz", style=style)
sim.saveDegreeDistribution("poi_tau2,5_degreedistr.tikz")
sim = SimulatingPoissonAlternative()
sim.generateGraph(25, 25, 0.625, 3.5, 3)
sim.draw(fp="poi_tau3,5.tikz", style=style)
sim.saveDegreeDistribution("poi_tau3,5_degreedistr.tikz")