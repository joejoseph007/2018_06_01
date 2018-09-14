Rmax=15
Rmin=5
Angle=36
Amax=5
Amin=-5
R_Lc=0.5
A_Lc=0.5
#per=0.1
l=8
t=8
Type="l"
MaxIt = 70 
nPop0 = 27    
nPop = 18
Smin = 0.5     
Smax = 3       
Exponent = 2
sigma_initial = 0.5
sigma_final = 0.01


nVar=180/Angle+2
Lim=[[[0,0],[0,0]] for i in range(nVar)] # [(Rmax,Rmin),(Amin,Amax)], constraint matrix


'''
for x in range(nVar):
	Lim[x][0][0]=Rmax
	Lim[x][0][1]=Rmin
	Lim[x][1][0]=x*Angle
	Lim[x][1][1]=(x-1)*Angle

Lim[0][1][1]=0
#Lim[0][1][0]=Amin

Lim[x][1][0]=180

for i in range(len(Lim)):
	print Lim[i] 
'''
'''
Values=[Rmax,Rmin,Amax,Amin,R_Lc,A_Lc,per,l,t,Type,MaxIt,nPop0,nPop,Smin,Smax,Exponent,sigma_initial,sigma_final]
Variables=['Rmax','Rmin','Amax','Amin','R_Lc','A_Lc','per','l','t','Type','MaxIt','nPop0','nPop','Smin','Smax','Exponent','sigma_initial','sigma_final']

#print Values,Variables
R=[]
for i in range(len(name)):
    for j in range(len(Values)):
        if name[i]==Variables[j]:
            R.append(Values[j])
'''
