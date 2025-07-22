'''given:
an directed graph G = (V,E,c) where V: the set of n nodes, E is the set of m edges in G, each edge e in E is associated
with a positive cost c(e)
# a pair of distinct nodes s and t in V
# a list L of k forbidden edge pairs, where each pair (e1,e2) belongs L satisfies e1,e2 belongs E
 ques: find an elementary path in G that starts at node s and ends at node t. visits each nodes
at most once, does not include both edges from any forgetbidden pair (e1,e2) belongs L and minimize the total cost of the path
input
line 1: contains 5 integers corresponding n,m,k,s,t (5 <= n<= 40)
 line i+1:(i =1,...,m) : each line contains three integers respresenting an edge in E, where the first two integers are the
endpoints of the edge, the third integer is the weight
 line i+m+1(i = 1,...k): each line contains four integers representing a forbidden pair of edges in L, where the first two
 integers are the endpoints of one edge, and the last two integers are the endpoints of the other edge in the pair
 Output: 
 line 1: total cost of the path(-1 if no feasible solution)
example:
input : 
7 18 2 1 0
2 1 115
6 5 175
6 2 200
4 3 149
6 1 155
5 6 179
0 4 125
4 1 124
2 3 155
5 4 107
4 2 172
6 4 175
4 6 103
1 6 121
3 2 132
3 6 103
4 0 197
2 0 138
2 1 0 4
5 6 4 3
output :
459'''
from ortools.sat.python import cp_model
import sys
import random as rd

'''def GenData(filename, n, m, s, t, M):
    with open(filename, 'w') as f:
        # Generate edges with unique (u, v) pairs
        E = []
        edge_set = set()
        while len(E) < m:
            u = rd.randint(0, n-1)
            v = rd.randint(0, n-1)
            if u != v and (u, v) not in edge_set:
                w = rd.randint(1, M)
                E.append((u, v, w))
                edge_set.add((u, v))
        
        # Generate conflict pairs from existing edges
        conflict_pairs = []
        if len(E) >= 2:
            all_pairs = []
            # Create all possible edge index pairs without repetition
            for i in range(len(E)):
                for j in range(i+1, len(E)):
                    all_pairs.append((i, j))
            rd.shuffle(all_pairs)
            k = rd.randint(0, len(all_pairs))  # Random number of conflict pairs up to max possible
            selected_pairs = all_pairs[:k]
            # Convert indices to actual edges
            for i, j in selected_pairs:
                e1 = E[i]
                e2 = E[j]
                conflict_pairs.append(f"{e1[0]} {e1[1]} {e2[0]} {e2[1]}")
        else:
            k = 0
        
        # Write header line (n, m, k, s, t)
        f.write(f"{n} {m} {k} {s} {t}\n")
        
        # Write edges
        for u, v, w in E:
            f.write(f"{u} {v} {w}\n")
        
        # Write conflict pairs
        for pair in conflict_pairs:
            f.write(f"{pair}\n")'''

def GenData(filename,n,m,s,t,M):
    with open(filename, 'w') as f:
        E=[]
        edge_set=set()
        while len(E)<m:
            u=rd.randint(0,n-1)
            v=rd.randint(0,n-1)
            if u!=v and (u,v) not in edge_set:
                w=rd.randint(1,M)
                E.append((u,v,w))
                edge_set.add((u,v))
        conflict=[]
        if len(E)>=2:
            all_pairs=[]
            #Create all index pairs distinct
            for i in range(len(E)):
                for j in range(i+1,len(E)):
                    all_pairs.append((i,j))
            rd.shuffle(all_pairs)
            k=rd.randint(0,int(len(all_pairs)/2))
            selected_pairs=all_pairs[:k]
            for (i,j) in selected_pairs:
                e1=E[i]
                e2=E[j]
                conflict.append(f"{e1[0]} {e1[1]} {e2[0]} {e2[1]}")
        else:
            k=0
        #Now write
        f.write(f"{n} {m} {k} {s} {t} \n")
        for (u,v,w) in E:
            f.write(f"{u} {v} {w} \n")
        for pair in conflict:
            f.write(f"{pair}\n")
GenData('Graph_with_forbid_paths.txt', 80,6000,1,0,10000)        
def Input():
    f=sys.stdin
    [n,m,k,s,t]=[int(x) for x in f.readline().split()]
    E=[]
    In=[[] for _ in range(n+1)]
    Out=[[] for _ in range(n+1)]
    for i in range(m):
        [u,v,w]=[int(x) for x in f.readline().split()]
        E.append([u,v,w])
        In[v].append([u,w])
        Out[u].append([v,w])
    #Forbidden
    [K]=[int(x) for x in f.readline().split()]
    L=[]
    for k in range(K):
        [a,b,c,d]=[int(x) for x in f.readline().split()]
        L.append([a,b,c,d])
    return n,m,s,t,E,In,Out,L
def inputfile(filename):
    with open(filename,'r') as f:
        [n,m,k,s,t]=[int(x) for x in f.readline().split()]
        E=[]
        In=[[] for _ in range(n+1)]
        Out=[[] for _ in range(n+1)]
        for i in range(m):
            [u,v,w]=[int(x) for x in f.readline().split()]
            E.append([u,v,w])
            In[v].append([u,w])
            Out[u].append([v,w])
        #Forbidden
        L=[]
        for _ in range(k):
           [a,b,c,d]=[int(x) for x in f.readline().split()]
           L.append([a,b,c,d])
    return n,m,s,t,E,In,Out,L
#n,m,s,t,E,In,Out,L=Input()
n,m,s,t,E,In,Out,L=inputfile('Graph_with_forbid_paths.txt')
model=cp_model.CpModel()
#Decision vars
x={}  #x[i,j]=1 if u->v is chosen
for [i,j,w] in E:
    x[i,j]=model.NewIntVar(0,1,'x('+str(i)+','+str(j)+')')
#Flow balance
for [i,j,w] in E:
    if i!=s and i!=t:
        model.Add(sum(x[i,j] for [j,w] in Out[i])==sum(x[j,i] for [j,w] in In[i]))
        model.Add(sum(x[i,j] for [j,w] in Out[i])<=1)
    model.Add(sum(x[s,i] for [i,w] in Out[s])==1)
    model.Add(sum(x[i,t] for [i,w] in In[t])==1)
#Forbidden avoid
for [a,b,c,d] in L:
    model.Add(x[a,b]+x[c,d]<=1)
#objective
obj=0
for [i,j,w] in E:
    obj+=w*x[i,j]
model.Minimize(obj)
solver=cp_model.CpSolver()
#solver.parameters.max_time_in_seconds=10.00
status=solver.Solve(model)    
if status==cp_model.OPTIMAL or status==cp_model.FEASIBLE:
    print('Optimal cost: ', solver.Value(obj))
    print('Optimal path: ')
    curr=s
    path=[curr]
    while curr!=t:
        for [i,j,w] in E:
            if i==curr and solver.Value(x[i,j])==1:
                path.append(j)
                curr=j
                break
    print('->'.join(map(str, path)))
else:
    print(-1)
print(f'Solved in {solver.WallTime():.2f} milliseconds, {solver.NumBranches()} branches.')
       
