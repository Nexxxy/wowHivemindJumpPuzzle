'''
Created on 10.01.2019

@author: ernstm
'''

import networkx as nx

def call_test(liste) :
    liste.append(6)
    return;

g = nx.MultiDiGraph()

g.add_node("a5")
g.add_node("a5b5")
g.add_node("a4a5b5")
g.add_node("a5a4")
g.add_node("null")

g.add_edge("a5","a5b5", label="F")
g.add_edge("a5","null", label="B")
g.add_edge("a5","null", label="L")
g.add_edge("a5","null", label="R")
g.add_edge("a5b5","null", label="F")
g.add_edge("a5b5","null", label="R")
g.add_edge("a5b5","null", label="L")
g.add_edge("a5b5","a4a5b5", label="B")

print (g["a5"]["null"])

print ("")


nx.write_gexf(g, "tst.gexf");


lst = [1,2,3,4,5]

call_test(lst.copy())

print (lst)

x = 15
y = [15, 12]

if (type(y) is list) :
    print ("liste")
else :
    print ("keine liste")


