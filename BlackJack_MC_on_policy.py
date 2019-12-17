### This scipt uses an on policy first visit Monte Carlo Approach ###

## Epsilon - Greedy Approach with a linear decay 
## It begins with a full exploration and stops exploring at 90% of the episodes

import os
import gym
import shutil 
import numpy as np
import Test_policy as tp
import scipy.io as sio
from tqdm import tqdm
from collections import defaultdict

env=gym.make('Blackjack-v0')

#%%#############################################################################

def target_policy_creation():

    ### This function creates a target policy - hit until 20 or 21 ###

    T=defaultdict(float)
    
    ace = [ False , True ]
    action = [ 0 , 1 ]
    
    for i in range (2,22):
        for j in range (1,12):
            for w in ace:
                for k in action:
                
                    ID = tuple([i,j,w])
                    
                    T[ID] = [0.5,0.5]
    return T

#%%#############################################################################


def convert_to_matlab(Q,T_P):
    
    Q_ = defaultdict(float)
    T_P_ = defaultdict(int)

    for key in Q.keys():
        
        Key_str = str(key)
        
        Q_[Key_str] = Q[key]
        
    for key_ in T_P.keys():
        
        Key_str_ = str(key_)
        
        T_P_[Key_str_] = T_P[key_]
        
    return Q_,T_P_

#%%#############################################################################

def policy (state,P):
    
### this function decides based on a policy vector which action to take###
        
    action = int(np.random.choice([0,1],1,p=P[state]))
    
    return action  

#%%#############################################################################

def game(env,states,actions,rewards,poli):
    
### this function runs an episode, meaning a single full game of BlackJack ###

    state = env.reset() # resets the enviroment and outpus the initial cards
    
    # this part eliminates the state which gives the dealers sum -
    # This part was changed from the GYM original
    
    done = False
    
    while not done: 
        
        states.append(state) # save state prior to game
        
        action = policy(state,poli) # define action based on a given policy
        
        actions.append(action) # save action taken 
                
        state, reward, done, info = env.step(action) # game instance - one action 
                
        rewards.append(reward) # save reward given 

    return states,actions,rewards

#%%#############################################################################


def first_visit_MC(numero,env,gamma):

    Q = defaultdict(float) # define an empty Q table
    
    Returns = defaultdict(list)

    P=target_policy_creation() # define the empty policy vector
    
    R=[]
                
    for i in tqdm( range (numero)):
    
        # create or clear variables 
        states = [] 
        actions = []
        rewards = []
        G = 0 
            
# =============================================================================
#         c = - np.log(0.1) / ( 0.9 * (numero) )
#         if i < numero:
#             eps = np.exp(-c*i)
#         else:
# =============================================================================
        eps = 0.15
            
        states,actions,rewards = game(env,states,actions,rewards,P)
        
        comp = (len(states))-1
        
        for j in range(comp,-1,-1): # run for every instance of an episode
        
    
            S_t = states[j]  # state to consider 
            R_t = rewards[j]
            A_t = actions[j]  # correspondent action
            
            S = list(S_t)
            A = [A_t]
            
            ID = tuple( S + A ) # associate state with action
                    
            A = tuple ( S + [0] )  # state com acção 0
            B = tuple ( S + [1] )  # states com acção 1
                        
            G = gamma*G + R_t # sum of rewards from each state and 
                                      
            if S_t not in states[:j]:
                
                Returns[ID].append(G)
                                              
                Q[ID] = np.average(Returns[ID])
                                
                if Q [A] > Q[B]:
                    A__ = 0
                else:
                    A__ = 1
                    
                if A__ == 0:
                    P[S_t]=[1 - eps + eps/2, eps/2]
                else:
                    P[S_t]=[eps/2, 1 - eps + eps/2]
                    
        R.append(sum(rewards))
                    
    return Q , P , R 

#%%#############################################################################

def convert_from_prob(P):
    
    P_=defaultdict(int)
    
    for key in P.keys():
                
        if P[key][0]>P[key][1]:
            P_[key] = 0
        else:
            P_[key] = 1
        
    return P_

#%%#############################################################################
    
num = 1

gamma = 0

Q , P , R  = first_visit_MC(int(num*1000000),env,gamma)

P1=convert_from_prob(P)

R_val, R_nl = tp.run_test_policy(P1,0.1)

Data = {}

Q_ , P_ = convert_to_matlab (Q,P1)

Data['Q'] = dict(Q_)
Data['Policy'] = dict(P_)
Data['R'] = list(R)
Data['R_total'] = R_val
Data['R_n_l'] = R_nl

filename = f'{num}_on_MC_control_g_{gamma}_eps_0.15.mat'

dr = os.getcwd() +'\Matlab\Dados'

sio.savemat(filename,Data)

shutil.move(filename,dr)
