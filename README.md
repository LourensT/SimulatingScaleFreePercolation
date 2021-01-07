# SimulatingScaleFreePercolation
Simulating Scale-free percolation graphs and exporting to .tikz (for LaTeX use)

 https://www.youtube.com/watch?v=JfqC-e6JsVk

## Dependencies
python package network2tikz is used:
`pip install network2tikz`

and tikzplotlib:
`pip install tikzplotlib`

the latex output depends on tikz-network, download the .sty here: https://mirror.lyrahosting.com/CTAN/graphics/pgf/contrib/tikz-network/tikz-network.sty

## Setting
Scale free percolation graph. parameters: lambda > 0 (percolation parameter), alpha > 0 (long range nature), tau (powerlaw exponent).

## How To Use
See the `ExampleUsage.py` for straightforward implementation.

## Example Output
Using v (averagedegrees) = 1, n (number of nodes) = 250, alpha (negative curvature) = 0.6, we obtain the following random graph:
![Example of random graph](https://github.com/LourensT/SimulatingScaleFreePercolation/blob/main/example.JPG)
