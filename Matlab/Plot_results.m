%%%%% Script to plot Results %%%%%%

clc
clear all

fprintf('Files in folder:')

dir

filename = input('Data filename:','s');

load(filename)

plot_BlackJack(Value)
plot_q (Q)
policy_plot(Policy)