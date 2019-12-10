### This scipt uses an on policy first visit Monte Carlo Approach ###

## Epsilon - Greedy Approach with a linear decay 
## It begins with a full exploration and stops exploring at 90% of the episodes

import gym
import scipy.io as sio
from collections import defaultdict

env=gym.make('Blackjack-v0')

#%%#############################################################################

def policy (state):
    
### this function decides based on a policy vector which action to take###
    
    state=list(state)
    
    if state[0] < 11: 
        
        action = 1
    else:
        action = 0 
            
    return action  

#%%#############################################################################

def game(env,states,actions,rewards,poli):
    
### this function runs an episode, meaning a single full game of BlackJack ###

    state = env.reset() # resets the enviroment and outpus the initial cards
    
    # this part eliminates the state which gives the dealers sum -
    # This part was changed from the GYM original
    state = list(state) 
    del state[2]
    state = tuple(state)
    
    done = False
    
    while not done: 
        
        states.append(state) # save state prior to game
        
        action = policy(state) # define action based on a given policy
        
        actions.append(action) # save action taken 
        
        state, reward, done, info = env.step(action) # game instance - one action 
        
        state = list(state)
        del state[2]    
        state = tuple(state)
                
        rewards.append(reward) # save reward given 

    return states,actions,rewards

#%%#############################################################################

def display_progress(numero,i,c):

## this function displays the progress of the program 

    if i == numero*0.01*c:
        
        per = str(c)
        percentage = per + '% - '
        
        print(percentage, end="")
        
        c += 1
        
    elif i == numero-1:
        
        print('100 % ', end="")
        
    
    return c

#%%#############################################################################

def first_visit_MC(numero,env):

    Q = defaultdict(float) # define an empty Q table
    Q_M = defaultdict(float) # define an empty Q - matlab
    V = defaultdict(float) # define an empty V - matlab

    P=defaultdict(int) # define the empty policy vector
    P_M=defaultdict(int) # define the empty policy vector - matlab
    
    cont_S_A= defaultdict(int) # define the contuer of single state - action pair
    cont_S= defaultdict(int) # define the counter of single states
    
    R=[] # reward vector to plot results
    
    c = 1 
        
    for i in range (numero):
        
        if numero > 100000:
            c = display_progress(numero,i,c) # display progress for large number of episodes
    
        # create or clear variables 
        states = [] 
        actions = []
        rewards = []
        Returns = 0 
    
        states,actions,rewards = game(env,states,actions,rewards,P)
        
        R.append(int(sum(rewards))) 

        comp = len(states)
    
        for j in range(comp): # run for every instance of an episode
            
            S_t = states[j]  # state to consider
            R_t = rewards[j]  # correspondent reward 
            A_t = actions[j]  # correspondent action
            
            S = list(S_t)
            A = [A_t]
            
            ID = tuple( S + A ) # associate state with action
            ID_str=str(ID)
                    
            A = tuple ( S + [0] )  # state com acção 0
            
            B = tuple ( S + [1] ) # states com acção 1
                        
            S_t_str=str(S_t)
            
            Returns += R_t # sum of rewards from each state and 
                          
            if S_t not in states[:j]:
                             
                cont_S_A[ID] += 1 
                cont_S[S_t_str] += 1 
                
                Q[ID] = ( Q[ID] * ( cont_S_A[ID] - 1) + (Returns) ) / cont_S_A[ID]
                Q_M [ID_str] = (Q_M [ID_str]*( cont_S_A[ID] - 1) + (Returns) ) / cont_S_A[ID]
                
                V [S_t_str] = ( V [S_t_str]*( cont_S[S_t_str] - 1) + (Returns) ) / cont_S[S_t_str]
                                                                    
    return Q , Q_M , V , R 

#%%#############################################################################
    
_ , Q_M , V, R = first_visit_MC(500000,env)

Data = {}

Data['Value'] = dict(V)
Data['Q']=dict(Q_M)
Data['Reward'] = R

filename = input('Done\nFilename:')

if filename !='':
    name = filename+'.mat'
                      
    sio.savemat(name,Data)
