#!/usr/bin/env python
# coding: utf-8

# In[ ]:
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

def network_iter(G,q,inf_init,N=4000,M=800,b=0.075,b2=0.06,gamma=0.2,neg_sen=0.85,delay=1): # N: total population, M: number of edge nodes
                                                             # P:testing period, Q: number of nodes being tested
                                                             # sensitivity: test accuracy
    counter = 0
    N_nodes = set(np.arange(0,N,1))

    test_list = random.sample(N_nodes,q)

    edges = random.sample(N_nodes,M)                     # randomly sample M edges nodes (boundary conditions) from whole population

    infected= inf_init                # randomly select 1 node from M edge nodes to be first infected
    suscep=[s for s in N_nodes if s not in infected]     # rest are susceptible

    removed=[]

    quarantine = []

    for inf in infected:                           #initialize node attribute
        G.nodes[inf]['status']='infected'
        G.nodes[inf]['inf_dur'] = 0             # used for counting infected duration
        G.nodes[inf]['test_day'] = None         # used for counting waiting time after the first test
        G.nodes[inf]['result'] = None           # used for tag the testing result

    for sus in suscep:
        G.nodes[sus]['status']='susceptible'
        G.nodes[sus]['test_day'] = None
        G.nodes[sus]['result'] = None
        G.nodes[sus]['inf_dur']= None

    gamma_inverse = 1/gamma
    I = 1
    S = N-I
    R = 0
    Q = 0
    dt = 1

    I_record=[1]
    S_record=[N-1]
    R_record=[0]
    Q_record=[0]
    TotalCases = I+R+Q
    finished = False
    peak_cases = 0
    peak_time = 0
    is_detected = False
    detected_day = 0

    # begin the loop
    while len(infected)>0:
        # After the detection the b will change to b2
        if finished == False:
            b = b
        elif finished == True:
            b = b2

        new_infected = []
        # calculate the infection probability for each node to simulate random in
        for sus in suscep:
            nei = G[sus].keys()       # get current susceptible's neighbors
            infected_nei = [n for n in nei if G.nodes[n]['status']=='infected']   # get infectious neighbors
            p_infection = 1-np.power((1-b*dt),len(infected_nei))    # get infectect probability for each node
            inf_status = np.random.binomial(1,p_infection)  # random function to decide whether this node will be infected
            if inf_status==1:
                new_infected.append(sus)
                I=I+1
                S=S-1

        new_removed = []

        # After gamma_inverse=5 days the I node will move to R
        for inf in infected:
            G.nodes[inf]['inf_dur']=G.nodes[inf]['inf_dur']+dt

            if G.nodes[inf]['inf_dur']>gamma_inverse:
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
            G.nodes[inf]['inf_dur'] = 0 # activate infected duration

        infected.extend(new_infected)
        removed.extend(new_removed)
        test_subjects = divide_test(counter,q,test_list)
        counter += 1

        G,N,S,I,R,Q,infected,quarantine,removed,suscep,finished,test_list = delay_test(G,N,dt,neg_sen,S,I,R,Q,
                                                                            test_subjects,delay,infected,
                                                                            quarantine,removed,suscep,
                                                                            finished,test_list)

        I_record.append(len(infected))
        R_record.append(len(removed))
        S_record.append(len(suscep))
        Q_record.append(len(quarantine))

        # Record the day when the first patient is detected
        if finished:
            if not is_detected:
                detected_day = counter
                is_detected = True

        # Record maximum of infected cases (I nodes) and that day
        TotalCases = len(infected)
        if TotalCases > peak_cases:
            peak_cases = TotalCases
            peak_time = counter

    return S_record,I_record,R_record,Q_record,peak_cases,peak_time,detected_day

def divide_test(counter,q,test_list):
    # In a testing period 7 days, all nodes in test_list (q parameter in our previous discussion)
    # will be tested. In the first 5 days in one testing period, nodes will be tested, while in the
    # last 2 days no nodes will be tested (considered as weekend).
    test_number = q//5
    if counter%7 < 4:
        return test_list[test_number*(counter%7):test_number*((counter+1)%7)]
    elif counter%7 == 4:
        return test_list[test_number*(counter%7):]
    elif counter%7 > 4:
        return []

def delay_test(G,N,dt,neg_sen,S,I,R,Q,test_subjects,delay,infected,quarantine,removed,suscep,finished,test_list):
    # In every iteration, the activate node (i.e. node with attribute "test_day" changing from None to 0)
    # will increase 1 day.
    for node in range(N):
        if str.isdigit(str(G.nodes[node]['test_day'])):
            G.nodes[node]['test_day'] += 1

    # When the node is tested, the result comes out immediately recorded in attribute "result",
    # while the result can only be checked by us, not nodes in the simulation. Since the "status"
    # doesn't change, the I node will keep infecting others while S node will keep being infected.
    # "test_day" changes from None to 0 to activate the testing node to the delaying-test list.
    for t in test_subjects:
        if G.nodes[t]['status'] in ['infected', 'removed']:
            G.nodes[t]['result'] = 'quarantined_pos'
            G.nodes[t]['test_day'] = 0
        if G.nodes[t]['status']=='susceptible':
            true_sus = np.random.binomial(1,neg_sen)
            if true_sus != 1:
                G.nodes[t]['result'] = 'quarantined_neg'
                G.nodes[t]['test_day'] = 0

    # When "test_day" reaches parameter "delay", "status" of this node will be changed to "quarantine"
    # if the result is positive.
    for node in range(N):
        if G.nodes[node]['test_day'] == delay:
            G.nodes[node]['test_day'] = None
            if G.nodes[node]['result'] == 'quarantined_pos':
                if G.nodes[node]['status'] == 'removed':
                    Q += 1
                    R -= 1
                    G.nodes[node]['status'] = 'quarantined'
                    quarantine.append(node)
                    removed.remove(node)
                elif G.nodes[node]['status'] == 'infected':
                    Q += 1
                    I -= 1
                    G.nodes[node]['status'] = 'quarantined'
                    quarantine.append(node)
                    infected.remove(node)
            elif G.nodes[node]['result'] == 'quarantined_neg':
                if G.nodes[node]['status'] == 'susceptible':
                    Q += 1
                    S -= 1
                    G.nodes[node]['status'] = 'quarantined'
                    quarantine.append(node)
                    suscep.remove(node)
                # Perhaps the susceptible node has already turned to infected
                elif G.nodes[node]['status'] == 'infected':
                    Q += 1
                    I -= 1
                    G.nodes[node]['status'] = 'quarantined'
                    quarantine.append(node)
                    infected.remove(node)
            finished = True
            test_list.remove(node)

    return G,N,S,I,R,Q,infected,quarantine,removed,suscep,finished,test_list


if __name__ == '__main__':
    delay_list = [1]#,2,3]
    b_list = [0.075]#,0.025,0.05,0.075]
    test_total = [800]#,2000,3600]

    for delay in delay_list:
        for b in b_list:
            b2 = (1/2)*b
            all_cases= []
            for test_pool in test_total:
                c1,c2,c3=[],[],[]
                for round in range(2):
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
                    init_inf = random.sample(infectious,1)
                    S,I,R,Q,peak_cases,peak_time,detected_day = network_iter(G,test_pool,init_inf,b=b,b2=b2,delay=delay)
                    c1.append(peak_cases)
                    c2.append(peak_time)
                    c3.append(detected_day)
                all_cases.append(c1)
                all_cases.append(c2)
                all_cases.append(c3)
                with open('delay_'+str(delay)+'_day_and_b_with_'+''.join(str(b).split('.'))+'_and_pool_'+str(test_pool)+'.pickle', 'wb') as f:
                    pickle.dump(all_cases,f)

    with open('delay_1_day_and_b_with_0075_and_pool_800.pickle', 'rb') as f:
        decrease1 = pickle.load(f)
    x=range(2)
    fig,ax = plt.subplots()
    average = np.mean(decrease1[0])
    plt1 = ax.bar(x=x,height=decrease1[0],label='before_b=0.075')
    ax.plot(x,[average]*2,color='red',label='average={}'.format(average))
    ax.set_xlabel('Simulation round')
    ax.set_ylabel('Peak cases')
    plt.xticks([index for index in x], x)
    ax.set_title('Delay 1 day testing with 20% population')
    ax.legend()
    ax.grid()
