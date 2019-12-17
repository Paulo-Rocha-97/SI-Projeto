import gym
from tqdm import tqdm
from collections import defaultdict

env=gym.make('Blackjack-v0')

def run_test_policy(poli,num): 
        
    R_total = []

    for i in tqdm(range (int(num*1000000))):
                
        states = []
        actions = []
        rewards = []
        
        state = env.reset() # resets the enviroment and outpus the initial cards
        
        done = False
        
        while not done: 
            
            states.append(state) # save state prior to game
            
            action = poli[state]
                          
            actions.append(action) # save action taken 
            
            state, reward, done, info = env.step(action) # game instance - one action 
                    
            rewards.append(reward) # save reward given 
            
        R_total.append(float(sum(rewards)))
        
    cont = 1
    cont_ok =1
        
    for k in range(len(R_total)):
        
        if R_total[k]==1:
            
            cont += 1
        
        if R_total[k]==1 or R_total[k]==0:
        
            cont_ok += 1    
        
    R_val = cont/(len(R_total))*100
    
    R_no_loss = cont_ok/(len(R_total))*100

    return R_val,R_no_loss

