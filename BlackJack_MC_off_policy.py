import gym
import numpy as np
import scipy.io as sio
from tqdm import tqdm
from collections import defaultdict

env=gym.make('Blackjack-v0')

#%%#############################################################################

def behaviour_policy_creation():
  
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
    state = list(state) 
    del state[2]
    state = tuple(state)
    
    done = False
    
    while not done: 
        
        states.append(state) # save state prior to game
        
        action = Behaviour_policy (state,B_P) # define action based on a given policy
        
        actions.append(action) # save action taken 
                
        state, reward, done, info = env.step(action) # game instance - one action 
        
        state = list(state)
        del state[2]    
        state = tuple(state)
                
        rewards.append(reward) # save reward given 

    return states,actions,rewards

#%%#############################################################################

def convert_to_matlab(Q,T_P):
    
    Q_ = defaultdict(float)
    T_P_ = defaultdict(float)

    for key in Q.keys():
        
        Key_str = str(key)
        
        Q_[Key_str] = Q[key]
        
    for key_ in Q.keys():
        
        Key_str_ = str(key_)
        
        T_P_[Key_str_] = T_P[key_]
        
    return Q_,T_P_


#%%#############################################################################

def MC_control(numero,env):
    
    
    B=behaviour_policy_creation()   # create behaviour policy
    
    gamma = 0.5

    Q = defaultdict(float)          # define an empty Q table
    C = defaultdict(float)          # define an empty C table

    T_P=defaultdict(int)            # define the empty policy vector
                
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
            S_hit = tuple(S+[1])
            S_skip = tuple(S+[0])
            
            ID=tuple(S+A)
            
            G = gamma*G + R_t                # sum of rewards from each state and 
                               
            C[ID] = C[ID] + W
                       
            Q[ID] = Q[ID] + (W/(C[ID])) * (G - Q[ID])
            
            if Q [S_hit] > Q[S_skip]:
                
                T_P[S_t] = 1
            else:
                T_P[S_t] = 0
                
            if T_P[S_t] == A_t:
                
                W = W * (1/B[S_t][A_t]) 
                                
    return Q , T_P 

#%%#############################################################################
    
Q , T_P = MC_control(2000000,env)

Data = {}

Q_ , T_P_ = convert_to_matlab (Q,T_P)

Data['Q']=dict(Q_)
Data['Policy'] = dict(T_P_)

filename = input('Done\nFilename:')

if filename !='':
    name = filename+'.mat'

    sio.savemat(name,Data)
