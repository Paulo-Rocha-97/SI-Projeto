function policy_plot(Policy)

valores=cell2mat(struct2cell(Policy));

nomes=fieldnames(Policy) ;

Cont_no = 1;
Cont_yes = 1;

for i = 1 : length(valores)
    
    var = split(nomes{i},[",",")","("]);
    
    if strcmp(var{4},' False')
        
        if str2num(var{2})>10 
            
            X_no(Cont_no) = str2num(var{2});
            Y_no(Cont_no) = str2num(var{3});
            Z_no(Cont_no) = valores(i);
            
            Cont_no = Cont_no + 1;
           
        end
    else
        if str2num(var{2})>10
            
            X(Cont_yes) = str2num(var{2});
            Y(Cont_yes) = str2num(var{3});
            Z(Cont_yes) = valores(i);
            
            Cont_yes = Cont_yes + 1;
        end
    end
end

comp = Cont_yes-1;
comp_no = Cont_no-1;

figure (5)
subplot(1,2,1)
title('Usable Ace')
for i = 1:comp 
    
    if Z(i)==1
        plot (Y(i),X(i),'ob')
    else
        plot (Y(i),X(i),'or')
    end
    hold on
end
title('Usable Ace')
hold off

subplot(1,2,2)
title('No Usable Ace')
for i = 1:comp_no 
    
    if Z_no(i)==1
        plot (Y_no(i),X_no(i),'ob')
    else
        plot (Y_no(i),X_no(i),'or')
    end
    hold on
end
title('No Usable Ace')
hold off


end