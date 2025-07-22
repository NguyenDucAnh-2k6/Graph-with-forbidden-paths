# Graph-with-forbidden-paths modeling
Given: <br />
an directed graph G = (V,E,c) where V: the set of n nodes, E is the set of m edges in G, each edge e in E is associated
with a positive cost c(e) <br />
a pair of distinct nodes s and t in V <br />
a list L of k forbidden edge pairs, where each pair (e1,e2) belongs L satisfies e1,e2 belongs E <br />
Objective: find an elementary path in G that starts at node s and ends at node t. visits each nodes <br />
at most once, does not include both edges from any forgetbidden pair (e1,e2) belongs to L and minimize the total cost of the path <br />
# Input  <br />
line 1: contains 5 integers corresponding n,m,k,s,t (5 <= n<= 40) <br />
line i+1:(i =1,...,m) : each line contains three integers respresenting an edge in E, where the first two integers are the
endpoints of the edge, the third integer is the weight <br />
line i+m+1(i = 1,...k): each line contains four integers representing a forbidden pair of edges in L, where the first two 
integers are the endpoints of one edge, and the last two integers are the endpoints of the other edge in the pair <br />
# Output: <br />
line 1: total cost of the path(-1 if no feasible solution) <br />
# Example: <br />
Input :  <br />
7 18 2 1 0 <br />
2 1 115 <br />
6 5 175 <br />
6 2 200 <br />
4 3 149 <br />
6 1 155 <br />
5 6 179 <br />
0 4 125 <br />
4 1 124 <br />
2 3 155 <br />
5 4 107 <br />
4 2 172 <br />
6 4 175 <br />
4 6 103 <br />
1 6 121 <br />
3 2 132 <br />
3 6 103 <br />
4 0 197 <br />
2 0 138 <br />
2 1 0 4 <br />
5 6 4 3 <br />
Output : <br />
459 
