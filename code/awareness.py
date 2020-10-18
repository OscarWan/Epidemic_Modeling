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
import multiprocessing as mp

def network_iter(G,Q,P,N=4000,M=800,b=0.1,gamma=0.2,c=0.2,kinit=20): # N: total population, M: number of edge nodes
                                                                    # P: testing period, Q: number of nodes being tested
                                                                    # c: awareness parameter, kinit: degree of initial infection node
    N_nodes = set(np.arange(0,N,1))

    test_subjects = random.sample(N_nodes,Q)             # randomly sample Q testing subjects from whole population

    # edges = random.sample(N_nodes,M)                     # randomly sample M edges nodes (boundary conditions) from whole population

    # fixed the initial node with certain degree
    not_empty = False
    while not not_empty:
        edges = random.sample(N_nodes,M)
        init_list = []
        for node in edges:
            if G.degree(node) == kinit:
                init_list.append(node)
                not_empty = True

    infected = random.sample(set(init_list),1)

    # infected= random.sample(set(edges),1)                # randomly select 1 node from M edge nodes to be first infected

    suscep=[s for s in N_nodes if s not in infected]     # rest are susceptible

    removed=[]

    for inf in infected:                           #initialize node attribute
        G.nodes[inf]['status']='infected'
        G.nodes[inf]['inf_dur']= 0
        G.nodes[inf]['ID']= 'None'

    for sus in suscep:
        G.nodes[sus]['status']='susceptible'
        G.nodes[sus]['ID']= 'None'

    for t in test_subjects:
        G.nodes[t]['ID']= 'Tested'

    # calculate distribution
    distribution = {}
    for node in G.nodes():
        k = G.degree(node)
        if k not in distribution:
            number = 1
            for temp in G.nodes():
                if temp != node and G.degree(temp) == k:
                    number += 1
            distribution[k] = number / N

    counter = 0

    gamma_inverse = 1/gamma
    I = 1
    S = N-I
    R = 0
    dt = 1

    I_record=[]
    S_record=[]
    R_record=[]
    TotalCases = I+R
    finished = False

    while len(infected)>0 and finished==False:

        new_infected = []

        # calculate awareness
        rho = 0
        for node in G.nodes():
            k = G.degree(node)
            nei = G[node].keys()
            infected_nei = [n for n in nei if G.nodes[n]['status']=='infected']
            rho_node = (len(infected_nei) / k) * distribution[k]
            rho += rho_node
        global_aware = max(1-c*rho,0)

        for sus in suscep:
            nei = G[sus].keys()       # get current susceptible's neighbors
            infected_nei = [n for n in nei if G.nodes[n]['status']=='infected']   # get infectious neighbors
            p_infection = 1-np.power((1-global_aware*b*dt),len(infected_nei))
            inf_status = np.random.binomial(1,p_infection)
            if inf_status==1:
                new_infected.append(sus)
                I=I+1
                S=S-1

        new_removed = []

        for inf in infected:

            G.nodes[inf]['inf_dur']=G.nodes[inf]['inf_dur']+dt

            if G.nodes[inf]['inf_dur']>=gamma_inverse:
                new_removed.append(inf)
                I=I-1
                R=R+1


        new_infected= list(dict.fromkeys(new_infected))
        new_removed = list(dict.fromkeys(new_removed))

        for re in new_removed:
            infected.remove(re)
            G.nodes[re]['status']='removed'

        for inf in new_infected:
            suscep.remove(inf)
            G.nodes[inf]['status']='infected'
            G.nodes[inf]['inf_dur']=0

        infected.extend(new_infected)
        removed.extend(new_removed)
        counter = counter + 1


        I_record.append(len(infected))
        R_record.append(len(removed))
        S_record.append(len(suscep))

        # # All testing nodes get tested at one time
        # if(counter % P == 0):
        #     for t in test_subjects:
        #         if (G.nodes[t]['status']=='infected' or G.nodes[t]['status']=='removed'):
        #             finished = True
        #             break

        # Divided into subgroup to get tested
        test_number = Q//P
        sub_test_group_ind = [(i+1)*test_number for i in range(P-1)]
        sub_test_group_ind.append(Q)
        for t in test_subjects[sub_test_group_ind[counter%P-1]:sub_test_group_ind[counter%P]]:
            if (G.nodes[t]['status']=='infected' or G.nodes[t]['status']=='removed'):
                finished = True
                break



    TotalCases = len(infected)+len(removed)

    return S_record,I_record,R_record,TotalCases
def fun(prob):
    N=4000           #population
    m=3
    G = nx.barabasi_albert_graph(N,m)               #create graph


    all_q = np.arange(10,1211,20)

    all_cases= []

    for i in range(len(all_q)):
        c= []
        for it in range(0,20):
            S,I,R,cases= network_iter(G,all_q[i],7,c=prob)  # Setting test period with 7 days
            c.append(cases)
        all_cases.append(np.mean(c))
    with open('test M '+str(prob)+' awareness', 'wb') as f:
        pickle.dump(all_cases, f)

if __name__ == '__main__':

    # all_P = np.array([2,4,7,9,10,12,14,16,19,21,24,28])
    all_prob = [0.002,0.0005,0.00005]
    jobs = []

    for prob in all_prob:

        p = mp.Process(target=fun, args=(prob,))
        jobs.append(p)
        p.start()


    for j in jobs:
        j.join()
sub_test_group_ind = [(i+1)*2 for i in range(7-1)]
print(sub_test_group_ind)
