import os
import gym
import shutil 
import numpy as np
import scipy.io as sio
import Test_policy as tp
from tqdm import tqdm
from collections import defaultdict

env=gym.make('Blackjack-v0')

#%%#############################################################################

def behaviour_policy_creation():

    ### This function creates a behaviour policy with a simple 50% chance in each state to garantee the coverage ###

    B=defaultdict(float)
    
    ace = [ False , True ]
    action = [ 0 , 1 ]
    
    for i in range (2,22):
        for j in range (1,12):
            for w in ace:
                for k in action:
                
                    ID = tuple([i,j,w])
                    
                    B[ID] = [0.5,0.5]
                    
    return B

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
                    
                    if i < 19:
                        T[ID] = [0,1]
                    else:
                        T[ID] = [1,0]
                    
    return T

#%%#############################################################################

def Behaviour_policy (state,B):
    
    action = np.random.choice([0,1],1,p=[B[state][0],B[state][1]]) 
    
    action = int(action)
        
    return action

#%%#############################################################################

def game(env,states,actions,rewards,B_P):
    
### this function runs an episode, meaning a single full game of BlackJack ###

    state = env.reset() # resets the enviroment and outpus the initial cards
    
    # this part eliminates the state which gives the dealers sum 
    # This was a changed from the GYM original
    
    done = False
    
    while not done: 
        
        states.append(state) # save state prior to game
        
        action = Behaviour_policy (state,B_P) # define action based on a given policy
        
        actions.append(action) # save action taken 
                
        state, reward, done, info = env.step(action) # game instance - one action 
                
        rewards.append(reward) # save reward given 

    return states,actions,rewards

#%%#############################################################################

def convert_to_matlab(Q):
    
    Q_ = defaultdict(float)

    for key in Q.keys():
        
        Key_str = str(key)
        
        Q_[Key_str] = Q[key]
                
    return Q_

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

def MC_eva(numero,env,gamma):
    
    
    B=behaviour_policy_creation()   # create behaviour policy
    T=target_policy_creation()
    
    Q = defaultdict(float)          # define an empty Q table
    C = defaultdict(float)          # define an empty C table
                
    for i in tqdm( range (numero)):
    
        # create or clear variables 
        states = [] 
        actions = []
        rewards = []
        G = 0 
        W = 1
        
        states,actions,rewards = game(env,states,actions,rewards,B)
        
        comp = (len(states))-1
        
        for j in range(comp,-1,-1): # run for every instance of an episode

            S_t = states[j]         # state to consider 
            R_t = rewards[j]        # correspondent action
            A_t = actions[j]        # correspondent action
            
            S=list(S_t)
            A=[A_t]
            
            ID=tuple(S+A)
            
            G = gamma*G + R_t                # sum of rewards from each state and 
                               
            C[ID] = C[ID] + W
                       
            Q[ID] = Q[ID] + (W/(C[ID])) * (G - Q[ID])
                
            W = W * (T[S_t][A_t]/B[S_t][A_t])
            
            if W == 0:
                break  
                           
    return Q ,T 

#%%#############################################################################
  
num = 1    
gamma = 1                 # gamma value 

Q ,P = MC_eva(int(num*1000000),env,gamma)

Data = {}

P1=convert_from_prob(P)

R_val, R_nl = tp.run_test_policy(P1,0.1)

Q_ = convert_to_matlab (Q)
P_ = convert_to_matlab (P1)

Data['Q']=dict(Q_)
Data['Policy'] = dict(P_)
    

filename = f'{num}_off_MC_eva_gamma_{gamma}.mat'

dr = os.getcwd() +'\Matlab\Dados'

sio.savemat(filename,Data)

shutil.move(filename,dr)