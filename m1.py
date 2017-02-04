
# coding: utf-8

# In[1]:

import copy

V=[[-10, -10,  0],
   [-10, -10, -10],
   [-10, -10, -10]]

R=[[0, 0, 0],
   [0, 0, 0],
   [0, 0, 0]]

print V
print R


# In[2]:

testV=[[-1, -2,  0],
   [-4, -5, -6],
   [-7, -8, -9]]

def argMax(V, R, x, y,cost=1):
    xmax = len(V[0])-1
    ymax = len(V)-1
    Vster = []
    Varror = []
    
    if x>0:
        Vster.append(V[y][x-1] - cost) 
        Varror.append("←")
    if x<xmax:
        Vster.append(V[y][x+1] - cost)
        Varror.append("→")
    if y>0:
        Vster.append(V[y-1][x] - cost)
        Varror.append("↑")
    if y<ymax:
        Vster.append(V[y+1][x] - cost)
        Varror.append("↓")
            
    Vster.append(V[y][x])
    Varror.append("・")
    
    #print Vster
    return max(Vster)-R[y][x], Varror[Vster.index(max(Vster))]

print argMax(testV,R,2,0)


# In[3]:

def kachihanpuku(V, R):
    Vpre = copy.deepcopy(V)
    Vster = [[0,0,0],[0,0,0],[0,0,0]]
    Varror = [[0,0,0],[0,0,0],[0,0,0]]
    firstFlag = 1
   
    #for i in range(5):
    while True:
        for x in range(len(V)):
            for y in range(len(V[x])):
                Vster[y][x],Varror[y][x] = argMax(Vpre, R, x, y)
        
        if Vpre == Vster:
            break
        Vpre = copy.deepcopy(Vster)
    return Vster, Varror

ans1, ans2 = kachihanpuku(V, R)
print ans1
print str(ans2).decode("string-escape")


# In[4]:

R1=[[0, 1, 0],
   [0, 0, 0],
   [0, 0, 0]]

R2=[[0, 10, 0],
   [0, 0, 0],
   [0, 0, 0]]
 
print str(kachihanpuku(V, R1)).decode("string-escape")
print "\n"
print str(kachihanpuku(V, R2)).decode("string-escape")


# In[117]:

print "→↑←↓"


# In[ ]:



