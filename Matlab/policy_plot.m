function policy_plot(Policy)

valores=cell2mat(struct2cell(Policy));

nomes=fieldnames(Policy) ;

Cont_no = 1;
Cont_yes = 1;

for i = 1 : length(valores)
    
    var = split(nomes{i},[",",")","("]);
    
    if strcmp(var{4},' False')
        
        if str2num(var{2})>10 && str2num(var{2})<22
            
            X_no(Cont_no) = str2num(var{2});
            Y_no(Cont_no) = str2num(var{3});
            Z_no(Cont_no) = valores(i);
            
            Cont_no = Cont_no + 1;
           
        end
    else
        if str2num(var{2})>10 && str2num(var{2})<22
            
            X(Cont_yes) = str2num(var{2});
            Y(Cont_yes) = str2num(var{3});
            Z(Cont_yes) = valores(i);
            
            Cont_yes = Cont_yes + 1;
        end
    end
end

comp = Cont_yes-1;
comp_no = Cont_no-1;

figure 
subplot(1,2,1)
for i = 1:comp 
    
    if Z(i)==1
       a = plot (Y(i),X(i),'ob');
    else
       b = plot (Y(i),X(i),'or');
    end
    hold on
end
xlabel("Dealer's card")
ylabel("Player's hand")
legend([a(1),b(1)],'Hit','Skip')
title('Usable Ace')
hold off

subplot(1,2,2)
for i = 1:comp_no 
    
    if Z_no(i)==1
       a_n = plot (Y_no(i),X_no(i),'ob');
    else
       b_n = plot (Y_no(i),X_no(i),'or');
    end
    hold on
end
xlabel("Dealer's card")
ylabel("Player's hand")
title('No Usable Ace')
legend([a_n(1),b_n(1)],'Hit','Skip')
hold off


end