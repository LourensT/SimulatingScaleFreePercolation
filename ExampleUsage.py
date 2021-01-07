import os
from SimulatingScaleFreePercolation import SimulatingScaleFreePercolation

style = ["\SetVertexStyle[MinSize=0.1\DefaultUnit, LineWidth=0pt, FillColor=mycolor1]\n", "\SetEdgeStyle[LineWidth=0.25pt]\n"]

sim = SimulatingScaleFreePercolation()
sim.generateGraph(25, 25, 0.625, 2.5, 3)
sim.draw(fp="tau2,5.tikz", style=style)
sim.saveDegreeDistribution("tau2,5_degreedistr.tikz")
sim.generateGraph(25, 25, 0.625, 3.5, 3)
sim.draw(fp="tau3,5.tikz", style=style)
sim.saveDegreeDistribution("tau3,5_degreedistr.tikz")