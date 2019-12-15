import gym
import numpy as np
import scipy.io as sio
from tqdm import tqdm
from collections import defaultdict

env=gym.make('Blackjack-v0')

#%%###########################################################################
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
#%%###########################################################################
def probability (numero,i):
    
### this function creates a decreasing probability of exploring - linear stops at 90% ###

    #parameterization of a exp
    c = - np.log(0.15) / 0.9 * (numero)
    if i < numero:
        eps = np.exp(-c*i)
    else:
        eps = 0.1
    explore = eps/2
    
    exploit = 1 - eps
    
    chosen = np.random.choice([0,1,2],1,p=[explore,explore,exploit]) # select if it should explore or exploit
    chosen = int(chosen)
            
    return chosen
#%%###########################################################################
def game_step(action):
    
    state_linha, reward, done, _ = env.step(action)
    
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
def sarsa_learning(env,numero,alpha,gamma):
    Q = defaultdict(float)
    P = defaultdict(int)

    for i in tqdm(range(numero)):
        C = probability (numero,i)
        S_t = env.reset()
        
        S_t = list(S_t)
        del S_t[2]
        S_t = tuple(S_t)
        
        done = False
        
        action = policy(S_t,P,C)
        
        while not done:
            
            S_t_linha, R_t , done = game_step(action)
            
            action_linha = policy(S_t_linha,P,C)
            
            S = list(S_t)
            S_linha = list(S_t_linha)
            
            A = [action]
            A_linha = [action_linha]
            
            ID = tuple(S + A)
            
            ID_stick = tuple(S + [0])
            ID_hit = tuple(S + [1])

            ID_linha = tuple(S_linha + A_linha)
                       
            if done:
                Q[ID_linha] = float(0)
            
            Q[ID] = Q[ID] + alpha*(R_t + gamma*Q[ID_linha] - Q[ID])
            
            if Q[ID_stick] > Q[ID_hit]:
                P[S_t] = 0
            else:
                P[S_t] = 1
            
            S_t = S_t_linha
            action = action_linha
                
    return Q
#%%########################################################################
Q = sarsa_learning(env,500000,0.1,0.8)

Data = {}

Q_=convert_to_matlab(Q)

Data['Q'] = dict(Q_)

filename = input('Done\nFilename:')

if filename !='':
    name = filename+'.mat'
                     
    sio.savemat(name,Data) 

