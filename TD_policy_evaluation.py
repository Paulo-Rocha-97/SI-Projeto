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
    
    state_linha, reward, done, _ = env.step(action)
    
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
        
        while True:
            
            action = policy(S_t)  
            
            S_t_1, R_t , done = game_step(action)
            
            if done:
                V_next=0
            else:
                V_next=V[S_t_1]
                
            V[S_t] = V[S_t] + alpha*(R_t + gamma*V_next - V[S_t])
            
            S_t = S_t_1
            
            if done:
                break
            
    return V
            
#%%########################################################################### 

num=1

gamma=1

alpha=0.05
V = td_0(env,int(num*1000000),alpha,gamma)

Data={}

V_=convert_to_matlab(V)

Data['V'] = dict(V_)
    
filename = f'{num}_TD_eva_a_{alpha}_g_{gamma}.mat'

dr = os.getcwd() +'\Matlab\Dados'

sio.savemat(filename,Data)

shutil.move(filename,dr)
