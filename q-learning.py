import os
import gym
import shutil
from numpy.random import choice
import Test_policy as tp
import scipy.io as sio
from tqdm import tqdm
from collections import defaultdict

env=gym.make('Blackjack-v0')

#%%###########################################################################

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
                    
                    T[ID] = [0.5,0.5]
    return T

#%%########################################################################### 

def convert_to_matlab(X):
    
    X_ = defaultdict(float)

    for key in X.keys():
        
        Key_str = str(key)
        
        X_[Key_str] = X[key]
        
    return X_

#%%########################################################################### 

def convert_from_prob(P):
    
    P_=defaultdict(int)
    
    for key in P.keys():
                
        if P[key][0]>P[key][1]:
            P_[key] = 0
        else:
            P_[key] = 1
        
    return P_
    
#%%###########################################################################
def q_learning(env,numero,alpha,gamma):
    
    Q = defaultdict(float)
    P = target_policy_creation()

    eps = 0.15;
    
    R = []

    for i in tqdm(range(numero)):

        S_t = env.reset()
                
        done = False
                
        while not done:
            
            action = int(choice([0,1],1,p=P[S_t]))
            
            S_t_linha, R_t , done, _ = env.step(action)
            
            S = list(S_t)
            S_linha = list(S_t_linha)
            A = [action]
            
            ID = tuple(S + A)
            
            ID_stick = tuple(S_linha + [0])
            ID_hit = tuple(S_linha + [1])
            ID_stick_ = tuple(S+ [0])
            ID_hit_ = tuple(S+ [1])
            
            if Q[ID_hit] > Q[ID_stick]:
                Q_max = Q[ID_hit]
            else:
                Q_max = Q[ID_stick]
           
            if done:
                Q_max = 0
                R.append(R_t)
            else:
                if Q[ID_hit] > Q[ID_stick]:
                    Q_max = Q[ID_hit]
                else:
                    Q_max = Q[ID_stick]
            
            Q[ID] = Q[ID] + alpha*(R_t + gamma*Q_max - Q[ID])
            
            if Q [ID_stick_] > Q[ID_hit_]:
                P[S_t]=[1 - eps + eps/2, eps/2]
            else:
                P[S_t]=[eps/2, 1 - eps + eps/2]
                
            
            S_t = S_t_linha
            
                
    return Q , P , R
#%%########################################################################
num=3

gamma=1

alpha=0.0005

Q, P, R = q_learning(env,int(num*1000000),alpha,gamma)

P1=convert_from_prob(P)

R_val, R_nl = tp.run_test_policy(P1,0.1)

Data = {}

Q_ = convert_to_matlab (Q)

P_ = convert_to_matlab(P1)

Data['Q'] = dict(Q_)
Data['Policy'] = dict(P_)
Data['R'] = list(R)
Data['R_total'] = R_val
Data['R_n_l'] = R_nl
   
filename = f'{num}_Q_a_{alpha}_g_{gamma}.mat'

dr = os.getcwd() +'\Matlab\Dados'

sio.savemat(filename,Data)

shutil.move(filename,dr)     