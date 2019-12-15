import os
import gym
import shutil 
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
    
    state_linha, reward, done = env.step(action)
    
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

    for i in tqdm(range(num)):
        
        S_t = env.reset()
        
        done = False
        
        while not done:
            
            action = policy(S_t)  
            
            S_t_1, R_t , done = game_step(action)
           
            if done:
                V_next=0
            else:
                V_next=V[S_t_1] 
          
            V[S_t] = (1-alpha)*V[S_t] + alpha*(R_t + gamma*V_next)
            
            S_t = S_t_1
            
    return V
            
#%%########################################################################### 

num=0.5

gamma=0

alpha=1

V = td_0(env,int(num*1000000),alpha,gamma)

Data={}

V_=convert_to_matlab(V)

Data['V'] = dict(V_)
    
filename = f'{num}_TD_eva_a_{alpha}_g_{gamma}.mat'

dr = os.getcwd() +'\Matlab\Dados'

sio.savemat(filename,Data)

shutil.move(filename,dr)

            
            
            
    
    