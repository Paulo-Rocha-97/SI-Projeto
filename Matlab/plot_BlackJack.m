function plot_BlackJack(Value)

valores=cell2mat(struct2cell(Value));

nomes=fieldnames(Value) ;

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

figure(1)
suptitle('Usable ace - Policy evaluation')
plot3(X,Y,Z,'.g')
grid on 
hold on
for i = 1:comp
   
    for j = 1:comp
        
       if X(i)==X(j) && abs(Y(i)-Y(j))==1 
           
           line([X(i) X(j)],[Y(i) Y(j)],[Z(i) Z(j)],"Color",'green')
           
       elseif Y(i)==Y(j) && abs(X(i)-X(j))==1
           
           line([X(i) X(j)],[Y(i) Y(j)],[Z(i) Z(j)],"Color",'green')
         
       end
        
    end
    
end
hold off


figure(2)
suptitle('No usable ace - Policy evaluation')
plot3(X_no,Y_no,Z_no,'.k')
grid on 
hold on
for i = 1:comp_no
   
    for j = 1:comp_no
        
       if X_no(i)==X_no(j) && abs(Y_no(i)-Y_no(j))==1 
           
           line([X_no(i) X_no(j)],[Y_no(i) Y_no(j)],[Z_no(i) Z_no(j)],'Color','black')

       elseif Y_no(i)==Y_no(j) && abs(X_no(i)-X_no(j))==1
           
           line([X_no(i) X_no(j)],[Y_no(i) Y_no(j)],[Z_no(i) Z_no(j)],'Color','black')

       end
        
    end
    
end
hold off


