import os
import gym
import shutil 
import scipy.io as sio
import Test_policy as tp
from tqdm import tqdm
from collections import defaultdict

env=gym.make('Blackjack-v0')
#%%########################################################################### 

def policy_creation():

    ### This function creates a target policy - hit until 20 or 21 ###

    T=defaultdict(float)
    
    ace = [ False , True ]
    
    for i in range (2,22):
        for j in range (1,12):
            for w in ace:                
                    ID = tuple([i,j,w])
                    
                    if i > 19:
                        T[ID] = 0    
                    else:
                        T[ID] = 1
    return T

#%%########################################################################### 

def convert_to_matlab(X):
    
    X_ = defaultdict(float)

    for key in X.keys():
        
        Key_str = str(key)
        
        X_[Key_str] = X[key]
        
    return X_

#%%########################################################################### 

def td_0(env,num,alpha,gamma):
    
    Policy = policy_creation()
    
    V = defaultdict(float)

    for i in tqdm(range(num)):
        
        S_t = env.reset()
        
        done = False
        
        while not done:
            
            action = Policy[S_t]  
            
            S_t_1, R_t, done, _ = env.step(action)
           
            if done:
                V_next=0
            else:
                V_next=V[S_t_1] 
          
            V[S_t] = (1-alpha)*V[S_t] + alpha*(R_t + gamma*V_next)
            
            S_t = S_t_1
                        
    return V , Policy
            
#%%########################################################################### 

num=1

gamma=1

alpha=0.0005

V , P = td_0(env,int(num*1000000),alpha,gamma)

R_val, R_nl = tp.run_test_policy(P,0.1)

Data={}

V_=convert_to_matlab(V)
P_=convert_to_matlab(P)

Data['V'] = dict(V_)
Data['Policy'] = dict(P_)
Data['R_total'] = R_val
Data['R_n_l'] = R_nl
    
filename = f'{num}_TD_eva_a_{alpha}_g_{gamma}.mat'

dr = os.getcwd() +'\Matlab\Dados'

sio.savemat(filename,Data)

shutil.move(filename,dr)
    