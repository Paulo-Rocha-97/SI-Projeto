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

def MC_control(numero,env,gamma):
    
    
    B=behaviour_policy_creation()   # create behaviour policy
    
    Q = defaultdict(float)          # define an empty Q table
    C = defaultdict(float)          # define an empty C table

    T_P = defaultdict(int)            # define the empty policy vector
    R=[]
                
    for i in tqdm( range (numero)):
    
        # create or clear variables 
        states = [] 
        actions = []
        rewards = []
        G = 0
        W = 1
        
        states,actions,rewards = game(env,states,actions,rewards,B)
        
        R.append(sum(rewards))
        
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
                
            else:
                break
                           
    return Q , T_P , R 

#%%#############################################################################
  
num = 5                    # numero de episodios em milhões     
gamma = 0.90                  # gamma value 

Q , P , R = MC_control(int(num*1000000),env,gamma)

P1=P

R_val, R_nl = tp.run_test_policy(P1,0.1)

Data = {}

Q_ , P_ = convert_to_matlab (Q,P1)

Data['Q'] = dict(Q_)
Data['Policy'] = dict(P_)
Data['R'] = list(R)
Data['R_total'] = R_val
Data['R_n_l'] = R_nl

filename = f'{num}_off_MC_control_g_{gamma}.mat'

dr = os.getcwd() +'\Matlab\Dados'

sio.savemat(filename,Data)

shutil.move(filename,dr)
