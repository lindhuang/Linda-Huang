INF = 99999     # distance magnitudes will not be larger than this number

def johnson(n, S):
    '''
    Input:  n | Number of vertices in the graph
            S | Tuple of triples (u, v, w) representing edge (u, v) of weight w
    Output: D | Tuple of tuples where D[u][v] is the distance from u to v
              |   or INF if v is not reachable from u
              |   or None if the input graph contains a negative-weight cycle
    '''
    D = [[INF for _ in range(n)] for _ in range(n)]
    adjlist={}
    weightmapping={}
    for num in range(n):
        adjlist[num]=[]
    for tupl in S:
        adjlist[tupl[0]].append(tupl[1])
        weightmapping[(tupl[0],tupl[1])]=tupl[2]
    def w(u,v):
        return weightmapping[(u,v)]
    
    adjlist[n]=list(range(n))
    for i in range(n):
        weightmapping[(n,i)]=0
    bellman=bellman_ford(adjlist, w, n)
    if bellman==None:
        return None
    
    bellman,parent=bellman
    weightmapping2={}
    for tupl in weightmapping:
        if tupl[0]==n:
            continue
        else:
            weightmapping2[tupl]=bellman[tupl[0]]+weightmapping[tupl]-bellman[tupl[1]]
            
    def w2(u,v):
        return weightmapping2[(u,v)]
    
    result=[]
    del adjlist[n]
    for vertice in range(n):
        lst=[]
        dij,parent=dijkstra(adjlist,w2,vertice)
        
        for index, value in enumerate(dij):
            if value==INF:
                lst.append(value)
            else:
                lst.append(value-bellman[vertice]+bellman[index])
        result.append(lst)
        

    D = tuple(tuple(row) for row in result)
    return D

####################################
# USE BUT DO NOT MODIFY CODE BELOW #
####################################
def bellman_ford(Adj, w, s):    # from R12
    '''
    Input: Adj | Direct access array mapping a vertex to a list of adjacencies
             w | Function w(u, v): weight of the edge from u to v
             s | Vertex where 0 <= s < |Adj|
    Output:  d | Direct access array mapping a vertex to distance from s
               |   or INF if v is not reachable from u
               |   or None if the input graph contains a negative-weight cycle
        parent | Direct access array mapping a vertex to parent on shortest path
    '''
    d = [INF for _ in Adj]
    parent = [None for _ in Adj]
    d[s], parent[s] = 0, None
    V = len(Adj)
    for k in range(V - 1):
        for u in range(V):
            for v in Adj[u]:
                if (d[v] > d[u] + w(u, v)) and (d[u] < INF):
                    d[v] = d[u] + w(u, v)
                    parent[v] = u
    for u in range(V):
        for v in Adj[u]:
            if d[v] > d[u] + w(u,v):
                return None
    return d, parent

def dijkstra(Adj, w, s):        # from R13
    '''
    Input: Adj | Direct access array mapping a vertex to a list of adjacencies
             w | Function w(u, v): non-negative weight of the edge from u to v
             s | Vertex where 0 <= s < |Adj|
    Output:  d | Direct access array mapping a vertex to distance from s
               |   or INF if v is not reachable from u
        parent | Direct access array mapping a vertex to parent on shortest path
    '''
    d = [INF for _ in Adj]
    parent = [None for _ in Adj]
    d[s], parent[s] = 0, None
    Q = PriorityQueue()
    V = len(Adj)
    for v in range(V):
        Q.insert(v, d[v])
    for _ in range(V):
        u = Q.extract_min()
        for v in Adj[u]:
            if (d[v] > d[u] + w(u, v)) and (d[u] < INF):
                d[v] = d[u] + w(u, v)
                parent[v] = u
            Q.decrease_key(v, d[v])
    return d, parent

class Item:
    def __init__(self, label, key):
        self.label, self.key = label, key

class PriorityQueue:
    def __init__(self):
        self.A = []
        self.label2idx = {}

    def min_heapify_up(self, c):            
        if c == 0: return
        p = (c - 1) // 2
        if self.A[p].key > self.A[c].key:   
            self.A[c], self.A[p] = self.A[p], self.A[c]         
            self.label2idx[self.A[c].label] = c
            self.label2idx[self.A[p].label] = p
            self.min_heapify_up(p)         

    def min_heapify_down(self, p):          
        if p >= len(self.A): return
        l = 2 * p + 1
        r = 2 * p + 2
        if l >= len(self.A): l = p
        if r >= len(self.A): r = p
        c = l if self.A[r].key > self.A[l].key else r 
        if self.A[p].key > self.A[c].key:             
            self.A[c], self.A[p] = self.A[p], self.A[c]         
            self.label2idx[self.A[c].label] = c
            self.label2idx[self.A[p].label] = p
            self.min_heapify_down(c)       

    def insert(self, label, key):
        self.A.append(Item(label, key))
        idx = len(self.A) - 1
        self.label2idx[self.A[idx].label] = idx
        self.min_heapify_up(idx)

    def extract_min(self):
        self.A[0], self.A[-1] = self.A[-1], self.A[0]
        self.label2idx[self.A[0].label] = 0
        del self.label2idx[self.A[-1].label]
        min_label = self.A.pop().label
        self.min_heapify_down(0)
        return min_label

    def decrease_key(self, label, key):
        if label in self.label2idx:
            idx = self.label2idx[label]
            if key < self.A[idx].key:
                self.A[idx].key = key
                self.min_heapify_up(idx)
