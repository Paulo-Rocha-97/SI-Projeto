%%%%% Script to plot Results %%%%%%

clc
clear all
close all

fprintf('Files in folder:')

dir Dados

filename = input('Data filename:','s');

if filename~=""
    
    directory = cd;
    
    s = strcat(directory,'\Dados');
    S = strcat(s,'\',filename);
    load(S)
    if exist('Q')==1
        plot_q (Q)
    end
    if exist('Policy')==1
        policy_plot(Policy)
    end
    if exist('V')==1
        plot_BlackJack(V)
    end
    if exist('R')==1
        plot_reward(R,R_n_l,R_total)
    end
end