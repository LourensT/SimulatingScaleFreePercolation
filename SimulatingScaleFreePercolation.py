import numpy as np
from scipy import stats
from Distribution import Distribution  #wrapper for stats distribution, samples bulkwise
import itertools
import networkx as nx
import network2tikz
import matplotlib.pyplot as plt
import datetime
import os
import tikzplotlib as plt2tikz

class SimulatingScaleFreePercolation:

    def __init__(self):
        #bulkwise sampler is quicker then sampling one by one
        #self.poissonSampler = Distribution(stats.poisson(poisson_mean)) 
        self.unifSampler = Distribution(stats.uniform())
        self.dir = ""

    def setOutputFolder(self, dir):
        assert os.path.isdir(dir), "checking if valid folder"
        self.dir = dir

    '''
    grid-wise generate vertices (following width, height)

    params:
    rows: number of rows
    columns: number of columns
    lam: weight parameter (avg degrees)
    tau: powerlaw exponent parameter

    '''
    def generateGraph(self, columns, rows, lam, tau, alpha):
        self.lam = lam
        self.tau = tau
        self.alpha = alpha

        #set new graph
        self.G = nx.Graph()
        #create new vertices on all 
        self.setVertices(columns, rows)
        for vertex in self.vertices:
            vertex.setWeight(self.sampleWeight())

        # add edges
        for (v1, v2) in itertools.combinations(self.vertices, r=2):
            if self.sampleEdge(v1, v2):
                self.G.add_edge(v1.id, v2.id)

        print('generated a graph with', str(columns*rows), 'vertices and', self.G.number_of_edges(), 'edges')
        
    '''
    sample a single weight (according to powerlaw distribution)
    '''
    def sampleWeight(self):
        print(self.lam *((self.unifSampler.rvs())**(-1/(self.tau -1))))
        return self.lam *((self.unifSampler.rvs())**(-1/(self.tau -1)))
            
    '''
    initializes the vertices, in this case according to 
    '''
    def setVertices(self, w, h):
        self.vertices = []
        id = 0
        for i in range(w):
            for j in range(h):
                self.vertices.append(Vertex(id, i, j))
                self.G.add_node(id)
                id += 1
    
    '''
    decide wether to add edge or not, based on weights
    '''
    def sampleEdge(self, v1, v2):
        dist = ((v1.x - v2.x)**2  + (v1.y - v2.y)**2)**(1/2)
        prob = 1 - np.exp(-self.lam*((v1.weight * v2.weight)**self.alpha) * (1/(dist**(self.alpha*2))) )
        if self.unifSampler.rvs() <= prob:
            return True
        else:
            return False

    '''
    returns euclidian distance between two points
    '''
    def calculateDistance(self, p1, p2):
        #p1= (r, angle), p2 = (r', angle')
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    '''
    output to tex and display graph
    '''
    def draw(self, fp="", style="", show = False, dump=True):
        #get default filepath
        if fp == "":
            fp = datetime.datetime.now().strftime("%Hh%Mm%Ss %d-%m-%Y") +".tikz"
        
        #get the positions of all nodes in euclidian coordinates
        layout = {v.id : (v.x, v.y) for v in self.vertices}
        #convert the network to tikz
        if dump:
            network2tikz.plot(self.G, self.dir+fp.replace('.tikz', '.tex'), layout=layout, canvas=(10,10))
            self.addStyleString(fp, style)

        #display the matplotlib view of the graph
        if show:
            nx.draw(self.G, pos=layout)
            plt.grid(True)
            plt.show()

    '''
    add the given style options to the output.tex at appropriate place
    '''
    def addStyleString(self, fp, style):
        #read in the output file and interlace the styling options
        allLines = []
        shouldSave = False #filter to only save the tikz picture
        with open(self.dir+fp.replace('.tikz', '.tex'), "r") as f:
            for line in f:
                if not shouldSave:
                    if "begin{tikzpicture}" in line: #start of tikzpicutre
                        for style_line in style:
                            allLines.append(style_line)
                        shouldSave = True
                if shouldSave:
                    allLines.append(line)
                    if "end{tikzpicture}" in line: #end of tikzpicutre
                        shouldSave = False

        #output the file again
        with open(self.dir+fp.replace('.tex', '.tikz'), "w") as f:
            for line in allLines:
                f.write(line)

        #remove original .tex file
        os.remove(self.dir+fp.replace('.tikz', '.tex'))   
    
    '''
    saves the degree distribution of the currently generated graph

    parameters: 
    fp: filepath to save file to
    show: whether to display the plot on screen
    '''
    def saveDegreeDistribution(self, fp, show=False):
        print("Saving: " + fp)
        assert ".tikz" in fp, "filepath does not end in .tikz"

        degrees = [self.G.degree(n) for n in self.G.nodes()]
        degrees.sort()
        total = sum(degrees)
        cumulative = [sum(degrees[n::])/total for n in range(len(degrees))]
        
        plt.loglog(degrees, cumulative)
        plt2tikz.save(self.dir+fp) #output

        if show:
            plt.show()
        
        plt.clf() #clear plot

class Vertex:
    weight = -1

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def setWeight(self, weight):
        self.weight = weight
    
    def getWeight():
        assert self.weight >= 0, "weight not yet set"
        return self.weight

if __name__ == "__main__":
    sim = SimulatingScaleFreePercolation()
    sim.generateGraph(25, 25, 0.625, 2.5, 3)
    sim.draw(show=True, dump=False)