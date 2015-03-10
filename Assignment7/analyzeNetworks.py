import sys
import requests
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def readEdgeList(filename):
    f = pd.read_csv(filename)
    rows = len(f)
    if f.shape >= (rows, 3):
        print 'Warning: edge list has more than two columns'

    edgeList = f[['0','1']]
    edgeFrame = pd.DataFrame(edgeList)

    return edgeFrame



def degree(edgeList, in_or_out):

    degree = 0

    if in_or_out == 'in':
        degree = edgeList['1'].value_counts()
        return degree
    elif in_or_out == 'out':
        degree = edgeList['0'].value_counts()
        return degree
    else:
        print 'Warning: Invalid Argument'



def combineEdgeLists(edgeList1, edgeList2):
    combination = [edgeList1, edgeList2]
    concatenated = pd.concat(combination)
    newEdge = pd.DataFrame.drop_duplicates(concatenated)

    return newEdge



def pandasToNetworkX(edgeList):
    diGraph = nx.DiGraph()
    edgeList = pd.DataFrame.to_records(edgeList, index = False)
    diGraph.add_edges_from(edgeList)
    return diGraph
#    nx.draw(diGraph)
#    plt.show()



def randomCentralNode(inputDiGraph):
    eigenDict = nx.eigenvector_centrality(inputDiGraph)
    raw = sum(eigenDict.values())
    factor = 1/raw
    newEigenDict = {key:value*factor for key, value in eigenDict.iteritems()}
    randomNode = np.random.choice(newEigenDict.keys(), p=newEigenDict.values())
    return randomNode




#For Testing the Functions
#edgeDogg = readEdgeList('Doggumentary')
#edgeLavigne = readEdgeList('The Best Damn Thing')
#snoopLavigne = combineEdgeLists(edgeDogg, edgeLavigne)
#graphDogg = pandasToNetworkX(edgeDogg)
#graphLavigne = pandasToNetworkX(edgeLavigne)
#print degree(edgeDogg,'in')
#print degree(edgeDogg,'out')
#print degree(edgeDogg,'stuff')
#print combineEdgeLists(edgeDogg, edgeLavigne)
#pandasToNetworkX(edgeDogg)
#pandasToNetworkX(edgeLavigne)
#pandasToNetworkX(snoopLavigne)
#print randomCentralNode(graphDogg)
