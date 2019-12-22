import numpy as np

numero =100

for i in range (numero):
    
    c = - np.log(0.15) / (0.9 * (numero))
    if i < 0.9*numero:
        eps = np.exp(-c*i)
    else:
        eps = 0.15
        
    print(eps)