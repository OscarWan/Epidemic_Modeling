import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import copy
from scipy.integrate import odeint
from scipy.optimize import root_scalar
import random
from bisect import bisect_right
import time
from mpmath import *
from mpl_toolkits import mplot3d
import pickle

# BA Graph Generation
N=4000           #population
m=3
G = nx.barabasi_albert_graph(N,m)               #create graph

infectious = []
N_nodes = set(np.arange(0,N,1))

for i in np.arange(1,300,3):
    s = set(n for n in N_nodes if len(G[n].keys())>=i and len(G[n].keys())<=i+2)
    if len(s)!=0:
        inf = random.sample(s,1)
        infectious.append(inf[0])
with open('G.pickle', 'wb') as f:
    pickle.dump(G, f)

with open('inf_sample.pickle', 'wb') as f:
    pickle.dump(infectious, f)

# ER Graph Generation
G = nx.random_graphs.erdos_renyi_graph(4000, 0.0025)
infectious = []
N_nodes = set(np.arange(0,N,1))

for i in np.arange(1,300,3):
    s = set(n for n in N_nodes if len(G[n].keys())>=i and len(G[n].keys())<=i+2)
    if len(s)!=0:
        inf = random.sample(s,1)
        infectious.append(inf[0])
with open('ER_G.pickle', 'wb') as f:
    pickle.dump(G, f)

with open('ER_inf_sample.pickle', 'wb') as f:
    pickle.dump(infectious, f)
