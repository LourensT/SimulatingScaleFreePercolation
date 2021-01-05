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

    def __init__(self, poisson_mean):
        #bulkwise sampler is quicker then sampling one by one
        self.poissonSampler = Distribution(stats.poisson(poisson_mean)) 
        self.unifSampler = Distribution(stats.unif())
        self.dir = ""

    def setOutputFolder(self, dir):
        assert os.path.isdir(dir), "checking if valid folder"
        self.dir = dir 

    def generateGraph(self, width, height):
        #set new graph
        self.G = nx.Graph()
        #
        self.samplePoints()

        # for all nodes
        for i in self.pointsPositions.keys():
            self.G.add_node(i)
        # add all edges between nodes if distance is smaller then radius
        for pair in itertools.combinations(self.pointsPositions.keys(), r=2):
            p1 = self.pointsPositions[pair[0]]
            p2 = self.pointsPositions[pair[1]]
            if self.calculateDistance(p1, p2) <= self.R:
                self.G.add_edge(pair[0], pair[1])

    def sampleWeights(self):
        print("generating weights")

    def setIntegerVertices(self, w, h):
        print("setting integer positions")
    
    '''
    decide whether to have edge between 
    '''
    def sampleEdge(self, weight1, weight2):
        return True

    '''
    returns euclidian distance between two points
    '''
    def calculateDistance(self, p1, p2):
        #p1= (r, angle), p2 = (r', angle')
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    '''
    output to tex and display graph
    '''
    def draw(self, fp="", style="", show = False):
        #get default filepath
        if fp == "":
            fp = datetime.datetime.now().strftime("%Hh%Mm%Ss %d-%m-%Y") +".tikz"
        
        #get the positions of all nodes in euclidian coordinates
        layout = self.pointsPositions.keys()
        #convert the network to tikz
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
