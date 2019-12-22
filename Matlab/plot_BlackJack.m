function plot_BlackJack(V)

valores=cell2mat(struct2cell(V));

nomes=fieldnames(V) ;

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
suptitle('Usable ace - Policy evaluation')
plot3(X,Y,Z,'.g')
view(-32,49)
xlabel("Player's hand")
ylabel("Dealer's card")
zlabel("Expected return")
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


figure
suptitle('No usable ace - Policy evaluation')
plot3(X_no,Y_no,Z_no,'.g')
view(-32,49)
xlabel("Player's hand")
ylabel("Dealer's card")
zlabel("Expected return")
grid on
hold on
for i = 1:comp_no
    
    for j = 1:comp_no
        
        if X_no(i)==X_no(j) && abs(Y_no(i)-Y_no(j))==1
            
            line([X_no(i) X_no(j)],[Y_no(i) Y_no(j)],[Z_no(i) Z_no(j)],'Color','green')
            
        elseif Y_no(i)==Y_no(j) && abs(X_no(i)-X_no(j))==1
            
            line([X_no(i) X_no(j)],[Y_no(i) Y_no(j)],[Z_no(i) Z_no(j)],'Color','green')
            
        end
        
    end
    
end
hold off


