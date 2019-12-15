import gym
import numpy as np
import scipy.io as sio
from tqdm import tqdm
from collections import defaultdict

env=gym.make('Blackjack-v0')

#%%########################################################################### 

def policy(state):
    if state[0] > 19:
        action = 0
    else:
        action = 1
    return action

#%%########################################################################### 

def game_step(action):
    
    state_linha, reward, done, info = env.step(action)
    
    state_linha = list(state_linha) 
    del state_linha[2]
    state_linha = tuple(state_linha)
    
    return state_linha, reward, done 

#%%########################################################################### 

def convert_to_matlab(V):
    
    V_ = defaultdict(float)

    for key in V.keys():
        
        Key_str = str(key)
        
        V_[Key_str] = V[key]
        
        
    return V_

#%%########################################################################### 

def td_0(env,num,alpha,gamma):
    
    V = defaultdict(float)
    error = []

    for i in tqdm(range(num)):
        
        S_t = env.reset()
        
        S_t=list(S_t)
        del S_t[2]
        S_t = tuple(S_t)
        
        done = False
        
        while not done:
            
            action = policy(S_t)  
            
            S_t_1, R_t , done = game_step(action)
            

# =============================================================================
#             if done:
#                 V[S_t_1] = float(0) 
# =============================================================================

            erro = alpha*(R_t + gamma*V[S_t_1] - V[S_t])
            V[S_t] = V[S_t] + alpha*(R_t + gamma*V[S_t_1] - V[S_t])
            
            error.append(abs(erro))
            S_t = S_t_1
            
    return V, error
            
#%%########################################################################### 

V, error = td_0(env,250000,0.1,0.8)

Data = {}

V_=convert_to_matlab(V)

Data['V'] = dict(V_)

filename = input('Done\nFilename:')

if filename !='':
    name = filename+'.mat'
                     
    sio.savemat(name,Data)

            
            
            
    
    