function plot_reward(R,R_n_l,R_total)

Intervalo = 0.0001;

passo = Intervalo*length(R);

c = 1;
cont = 1;
cnt =1; 
Comp=(1/Intervalo);

Vic =  zeros(1,Comp);
Vic_emp =  zeros(1,Comp);
R_total_ =  zeros(1,Comp);
R_n_l_ =  zeros(1,Comp);

for i = 1 : length(R) 
    
    if passo*c == i 
        Vic(c)=(cont/i)*100;
        Vic_emp(c)=100-(cnt/i)*100;
        R_total_(c)= R_total;
        R_n_l_(c)= 100-R_n_l;
        c=c+1;
    end

    if R(i)==1
        cont=cont+1;
    end
    if R(i)==1 || R(i)==0
        cnt=cnt+1;
    end
        
end

figure
loglog (Vic,'b','DisplayName','Victories while training')
hold on
loglog (Vic_emp,'r','DisplayName','Losses while trainig')
loglog (R_total_,'--b','DisplayName','Victories after training')
loglog (R_n_l_,'--r','DisplayName','Losses after training')
ylim([30 70])
a=[10^0 , 10^1 10^2 10^3 10^4]*(length(R)/10000);
b= num2cell(a);
xticks([10^0 10^1 10^2 10^3 10^4])
xticklabels(b)
xlabel('Iteractions')
ylabel('Percentage')
title('Percentage of Rewards along training')
legend
hold off
grid on


end