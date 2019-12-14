### This scipt uses an on policy first visit Monte Carlo Approach ###

## Epsilon - Greedy Approach with a linear decay 
## It begins with a full exploration and stops exploring at 90% of the episodes

import gym
import numpy as np
import scipy.io as sio
from tqdm import tqdm
from collections import defaultdict

env=gym.make('Blackjack-v0')

#%%#############################################################################

def policy (state,poli,C):
    
### this function decides based on a policy vector which action to take###
    
    state=list(state)
    
    if state[0] < 11:  # value benneath which it does not make sense other action 
        action = 1
        
    else:
        
        if C == 2:
                
            state = tuple(state) 
            action = poli[state] # action following the policy defined
            
        else:
            action = C  
        
    #action = env.action_space.sample()
    
    return action  

#%%#############################################################################

def game(env,states,actions,rewards,poli,C):
    
### this function runs an episode, meaning a single full game of BlackJack ###

    state = env.reset() # resets the enviroment and outpus the initial cards
    
    # this part eliminates the state which gives the dealers sum -
    # This part was changed from the GYM original
    state = list(state) 
    del state[2]
    state = tuple(state)
    
    done = False
    
    while not done: 
        
        states.append(state) # save state prior to game
        
        action = policy(state,poli,C) # define action based on a given policy
        
        actions.append(action) # save action taken 
                
        state, reward, done, info = env.step(action) # game instance - one action 
        
        state = list(state)
        del state[2]    
        state = tuple(state)
                
        rewards.append(reward) # save reward given 

    return states,actions,rewards

#%%#############################################################################

def probability (numero,i):
    
### this function creates a decreasing probability of exploring - linear stops at 90% ###

    #parameterization of a exp
    c = - np.log(0.1) / 0.9 * (numero)
    if i < numero:
        eps = np.exp(-c*i)
    else:
        eps = 0.1
    explore = eps/2
    
    exploit = 1 - eps
    
    chosen = np.random.choice([0,1,2],1,p=[explore,explore,exploit]) # select if it should explore or exploit
    chosen = int(chosen)
            
    return chosen 

#%%#############################################################################


def first_visit_MC(numero,env):

    Q = defaultdict(float) # define an empty Q table
    Q_M = defaultdict(float) # define an empty Q - matlab
    Returns = defaultdict(int)

    P=defaultdict(int) # define the empty policy vector
    P_M=defaultdict(int) # define the empty policy vector - matlab
    
    cont_S_A= defaultdict(int) # define the contuer of single state - action pair
    cont_S= defaultdict(int) # define the counter of single states
    
    R=[] # reward vector to plot results
        
    for i in tqdm( range (numero)):
    
        # create or clear variables 
        states = [] 
        actions = []
        rewards = []
        G = 0 
        
        C = probability (numero,i)
    
        states,actions,rewards = game(env,states,actions,rewards,P,C)
        
        R.append(int(sum(rewards))) 

        comp = (len(states))-1
        
        for j in range(comp,-1,-1): # run for every instance of an episode

            S_t = states[j]  # state to consider 
            R_t = rewards[j]
            A_t = actions[j]  # correspondent action
            
            S = list(S_t)
            A = [A_t]
            
            ID = tuple( S + A ) # associate state with action
            ID_str=str(ID)
                    
            A = tuple ( S + [0] )  # state com acção 0
            
            B = tuple ( S + [1] ) # states com acção 1
                        
            S_t_str=str(S_t)

            G += R_t # sum of rewards from each state and 

                                      
            if S_t not in states[:j]:
                
                Returns[ID] +=  G
                              
                cont_S_A[ID] += 1 
                cont_S[S_t_str] += 1 
                
                Q[ID] = Returns[ID] / cont_S_A[ID]
                Q_M [ID_str] = Returns[ID]  / cont_S_A[ID]
                                
                if Q [A] > Q[B]:
                    P[S_t] = 0
                    P_M[S_t_str] = 0 
                else:
                    
                    P[S_t] = 1
                    P_M[S_t_str] = 1 
                    
                
                
    return Q , Q_M , P , P_M , R 

#%%#############################################################################
    
_ , Q_M , _ , P_M, R = first_visit_MC(500000,env)

Data = {}

Data['Q']=dict(Q_M)
Data['Policy'] = dict(P_M)
Data['Reward'] = R

filename = input('Done\nFilename:')

if filename !='':
    name = filename+'.mat'

    sio.savemat(name,Data)

