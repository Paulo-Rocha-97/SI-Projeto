function alpha_calc

%%%%%this function compares values of the different TD alpha policy evaluation

%%%%uses only the no usable ace values

directory = cd;

name = ["1_TD_eva_a_0.5_g_1.mat" , "1_TD_eva_a_0.05_g_1.mat","1_TD_eva_a_0.005_g_1.mat","1_TD_eva_a_0.0005_g_1.mat","1_TD_eva_a_5e-05_g_1.mat","1_TD_eva_a_5e-06_g_1.mat","1_TD_eva_a_5e-07_g_1.mat","1_TD_eva_a_0_g_1.mat"];
alpha = [0.5,0.05,0.005,0.0005,0.00005,0.000005,0.0000005,0];

compare = "1_MC_eva_.mat";

s = strcat(directory,'\Dados');
S = strcat(s,'\',compare);
load(S)

Vcomp=V;

valores_comp=cell2mat(struct2cell(Vcomp));

nomes_comp=fieldnames(Vcomp) ;

Cont_no = 1;
Cont_yes = 1;

for i = 1 : length(valores_comp)
    
    var = split(nomes_comp{i},[",",")","("]);
    
    if strcmp(var{4},' False')
        
        if str2num(var{2})>10 && str2num(var{2})<22
            
            X_no_comp(Cont_no) = str2num(var{2});
            Y_no_comp(Cont_no) = str2num(var{3});
            Z_no_comp(Cont_no) = valores_comp(i);
            
            Cont_no = Cont_no + 1;
            
        end
    else
        if str2num(var{2})>10 && str2num(var{2})<22
            
            X_comp(Cont_yes) = str2num(var{2});
            Y_comp(Cont_yes) = str2num(var{3});
            Z_comp(Cont_yes) = valores_comp(i);
            
            Cont_yes = Cont_yes + 1;
        end
    end
    
    
end

Var_value_no=zeros(1,length(name));

Var_value=zeros(1,length(name));

for i = 1:length(name)
    
    s = strcat(directory,'\Dados');
    S = strcat(s,'\',name(i));
    load(S)
    
    
    valores=cell2mat(struct2cell(V));
    
    nomes=fieldnames(V) ;
    
    Cont_no = 1;
    Cont_yes = 1;
    
    for j = 1 : length(valores)
        
        var = split(nomes{j},[",",")","("]);
        
        if strcmp(var{4},' False')
            
            if str2num(var{2})>10 && str2num(var{2})<22
                
                X_no(Cont_no) = str2num(var{2});
                Y_no(Cont_no) = str2num(var{3});
                Z_no(Cont_no) = valores(j);
                
                Cont_no = Cont_no + 1;
                
            end
        else
            if str2num(var{2})>10 && str2num(var{2})<22
                
                X(Cont_yes) = str2num(var{2});
                Y(Cont_yes) = str2num(var{3});
                Z(Cont_yes) = valores(j);
                
                Cont_yes = Cont_yes + 1;
            end
        end
        
        
    end
    
    cont_n=1;
    
    for k = 1:110
    
        for m =1:110
           
            if X_no(k)==X_no_comp(m) && Y_no(k)==Y_no_comp(m)
                
                Var_value_no(i)=(Var_value_no(i)*(cont_n-1) + (( Z_no(k) - Z_no_comp(m) )^2 ) )/cont_n;   
                  
                cont_n= cont_n+1;
                
            end
        end
       cont_n; 
    end
    
    cont_n=1;
    
    for k = 1:100
    
        for m =1:100
           
            if X(k)==X_comp(m) && Y(k)==Y_comp(m)
                
                Var_value(i)=(Var_value_no(i)*(cont_n-1) + (( Z(k) - Z_comp(m) )^2 ) )/cont_n;   
                  
                cont_n= cont_n+1;
                
            end
        end
       cont_n; 
    end
    
end

figure 
hold on
plot(Var_value,'--og','DisplayName','Usable ace')
plot(Var_value_no,'--or','DisplayName','No usable ace')
ylabel('Variance compared with MC method')
xlabel('Alpha')
xticks([1,2,3,4,5,6,7,8])
xticklabels({'5e(-1)','5e(-2)','5e(-3)','5e(-4)','5e(-5)','5e(-6)','5e(-7)','0'})
legend
grid on

end