function plot_q (Q)

valores=cell2mat(struct2cell(Q));

nomes=fieldnames(Q) ;

Cont_no_0 = 1;
Cont_no_1 = 1;
Cont_yes_0 = 1;
Cont_yes_1 = 1;

for i = 1 : length(valores)
    
    var = split(nomes{i},[",",")","("]);
    
    if strcmp(var{4},' False')
        
        if str2num(var{2})>10 && str2num(var{5})==1
            
            X_no_1(Cont_no_1) = str2num(var{2});
            Y_no_1(Cont_no_1) = str2num(var{3});
            Z_no_1(Cont_no_1) = valores(i);
            
            Cont_no_1 = Cont_no_1 + 1;
            
        elseif str2num(var{2})>10 && str2num(var{5})==0
            
            X_no_0(Cont_no_0) = str2num(var{2});
            Y_no_0(Cont_no_0) = str2num(var{3});
            Z_no_0(Cont_no_0) = valores(i);
            
            Cont_no_0 = Cont_no_0 + 1;
            
        end
    else
        if str2num(var{2})>10 && str2num(var{5})==1
            
            X_1(Cont_yes_1) = str2num(var{2});
            Y_1(Cont_yes_1) = str2num(var{3});
            Z_1(Cont_yes_1) = valores(i);
            
            Cont_yes_1 = Cont_yes_1 + 1;
            
        elseif str2num(var{2})>10 && str2num(var{5})==0
            
            X_0(Cont_yes_0) = str2num(var{2});
            Y_0(Cont_yes_0) = str2num(var{3});
            Z_0(Cont_yes_0) = valores(i);
            
            Cont_yes_0 = Cont_yes_0 + 1;
        end
    end
end % write values in vectors

comp_1 = Cont_yes_1-1;
comp_0 = Cont_yes_0-1;

comp_no_1 = Cont_no_1-1;
comp_no_0 = Cont_no_0-1;

figure(3)
suptitle('Usable ace - Q(S_t)(A_t)')
plot3(X_1,Y_1,Z_1,'.b') % plot usable ace kind 
grid on 
hold on
for i = 1:comp_1
   
    for j = 1:comp_1
        
       if X_1(i)==X_1(j) && abs(Y_1(i)-Y_1(j))==1 
           
           line([X_1(i) X_1(j)],[Y_1(i) Y_1(j)],[Z_1(i) Z_1(j)],'Color','blue')
           
       elseif Y_1(i)==Y_1(j) && abs(X_1(i)-X_1(j))==1
           
           line([X_1(i) X_1(j)],[Y_1(i) Y_1(j)],[Z_1(i) Z_1(j)],'Color','blue')
         
       end
        
    end
    
end % create grid lines
plot3(X_0,Y_0,Z_0,'.r')
for i = 1:comp_0
   
    for j = 1:comp_0
        
       if X_0(i)==X_0(j) && abs(Y_0(i)-Y_0(j))==1 
           
           line([X_0(i) X_0(j)],[Y_0(i) Y_0(j)],[Z_0(i) Z_0(j)],'Color','red')
           
       elseif Y_0(i)==Y_0(j) && abs(X_0(i)-X_0(j))==1
           
           line([X_0(i) X_0(j)],[Y_0(i) Y_0(j)],[Z_0(i) Z_0(j)],'Color','red')
         
       end
        
    end
    
end % create grid lines

hold off


figure(4)
suptitle('No usable ace - Q(S_t)(A_t)')
plot3(X_no_1,Y_no_1,Z_no_1,'.b')
grid on 
hold on
for i = 1:comp_no_1
   
    for j = 1:comp_no_1
        
       if X_no_1(i)==X_no_1(j) && abs(Y_no_1(i)-Y_no_1(j))==1 
           
           line([X_no_1(i) X_no_1(j)],[Y_no_1(i) Y_no_1(j)],[Z_no_1(i) Z_no_1(j)],'Color','blue')
           
       elseif Y_no_1(i)==Y_no_1(j) && abs(X_no_1(i)-X_no_1(j))==1
           
           line([X_no_1(i) X_no_1(j)],[Y_no_1(i) Y_no_1(j)],[Z_no_1(i) Z_no_1(j)],'Color','blue')
         
       end
        
    end
    
end
plot3(X_no_0,Y_no_0,Z_no_0,'.r')
for i = 1:comp_no_0
   
    for j = 1:comp_no_0
        
       if X_no_0(i)==X_no_0(j) && abs(Y_no_0(i)-Y_no_0(j))==1 
           
           line([X_no_0(i) X_no_0(j)],[Y_no_0(i) Y_no_0(j)],[Z_no_0(i) Z_no_0(j)],'Color','red')
           
       elseif Y_no_0(i)==Y_no_0(j) && abs(X_no_0(i)-X_no_0(j))==1
           
           line([X_no_0(i) X_no_0(j)],[Y_no_0(i) Y_no_0(j)],[Z_no_0(i) Z_no_0(j)],'Color','red')
         
       end
        
    end
    
end
hold off


