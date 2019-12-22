### This scipt uses an on policy first visit Monte Carlo Approach ###

## Epsilon - Greedy Approach with a linear decay 
## It begins with a full exploration and stops exploring at 90% of the episodes

import os
import gym
import shutil 
import Test_policy as tp
import scipy.io as sio
from tqdm import tqdm
from collections import defaultdict

env=gym.make('Blackjack-v0')

#%%#############################################################################

def convert_to_matlab(X,Y):
    
    X_ = defaultdict(float)

    for key in X.keys():
        
        Key_str = str(key)
        
        X_[Key_str] = X[key]
        
    Y_ = defaultdict(float)

    for key in Y.keys():
        
        Key_str = str(key)
        
        Y_[Key_str] = Y[key]

        
    return X_,Y_
    
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
                    
                    if i < 20:
                        T[ID] = int(1)
                    else:
                        T[ID] = int(0)
                    
    return T

#%%#############################################################################

def policy (state,T_P):
    
### this function decides based on a policy vector which action to take###
    
    action = T_P[state]
            
    return action  

#%%#############################################################################

def game(env,states,actions,rewards,T_P):
    
### this function runs an episode, meaning a single full game of BlackJack ###

    state = env.reset() # resets the enviroment and outpus the initial cards
    
    done = False
    
    while not done: 
        
        states.append(state) # save state prior to game
        
        action = policy(state,T_P) # define action based on a given policy
        
        actions.append(action) # save action taken 
        
        state, reward, done, info = env.step(action) # game instance - one action 
                
        rewards.append(reward) # save reward given 

    return states,actions,rewards

#%%#############################################################################

def first_visit_MC(numero,env):
    
    T_P=target_policy_creation()

    V = defaultdict(float) # define an empty V - matlab
        
    cont_S= defaultdict(int) # define the counter of single states
            
    for i in tqdm(range (numero)):
    
        # create or clear variables 
        states = [] 
        actions = []
        rewards = []
        G = 0 
    
        states,_,rewards = game(env,states,actions,rewards,T_P)
        
        comp = len(states)-1
    
        for j in range(comp,-1,-1): # run for every instance of an episode
            
            S_t = states[j]  # state to consider
            R_t = rewards[j]  # correspondent reward 
                                                
            G += R_t # sum of rewards from each state and 
                          
            if S_t not in states[:j]:
                
                cont_S[S_t]=cont_S[S_t]+1
                             
                V [S_t] = ( V [S_t]*( cont_S[S_t] - 1) + (G) ) / cont_S[S_t]
                                                                    
    return V , T_P

#%%#############################################################################
    
num = 5    

V , T_P = first_visit_MC(int(num*1000000),env)

R_val, R_nl = tp.run_test_policy(T_P,0.1)

Data = {}

V_ , T_P_  = convert_to_matlab (V,T_P)

Data['V'] = dict(V_)
Data['Policy'] = dict(T_P_)
Data['R_total'] = R_val
Data['R_n_l'] = R_nl
    
filename = f'{num}_MC_eva_.mat'

dr = os.getcwd() +'\Matlab\Dados'

sio.savemat(filename,Data)

shutil.move(filename,dr)