import numpy as np

def get_elimination_order(AdjMatr):
    Matrix = AdjMatr.copy()
    elimination_order = []
    added_connections = []
    ids_list = np.arange(AdjMatr.shape[0])
    for i in range(Matrix.shape[0]-1):
        vertex_degrees = np.zeros(Matrix.shape[0])        
        for i in range(Matrix.shape[0]):
            for j in range(Matrix.shape[1]):
                if Matrix[i][j] == 1:
                    vertex_degrees[i] += 1
        vertex_degrees[vertex_degrees==0] = np.inf
        min_degree_id = np.argmin(vertex_degrees)
        elimination_order.append(min_degree_id)
        np.delete(ids_list,min_degree_id)
        removed_connections = []
        for i in range(Matrix.shape[0]):
            if Matrix[min_degree_id,i]==1:
                removed_connections.append(i)
                Matrix[min_degree_id,i] = 0
                Matrix[i,min_degree_id] = 0
        for node1 in removed_connections:
            for node2 in removed_connections:
                if node1 != node2:
                    Matrix[node1,node2] = 1
                    Matrix[node2,node1] = 1
                    added_connections.append([node1,node2])
                    added_connections.append([node2,node1])
    for i in ids_list:
        if i not in elimination_order:
            elimination_order.append(i)
    return elimination_order,added_connections

def get_fill_in_graph(AdjMatr,added_connections):
    Matrix = AdjMatr.copy()
    for node1,node2 in added_connections:
        Matrix[node1,node2] = 1
    return Matrix

def get_labelling(elimination_order,AdjMatr):
    order = elimination_order[::-1]
#    traversing elimination order in reverse order
#creating dictionaries for labels and parents; i.e. key, node pairs => vertex_id, shortest_distance, 
    labels = {}
    parents = {}
    for i in range(len(order)):
        C = []
        for j in elimination_order:
            if AdjMatr[order[i],j]==1:  #check if vertex checked from higher ordered nodes in elimination order is a neighbor of target vertex
                if j in order[:i]:
                    C.append(j)
        ls = [(j,shortest_distance(AdjMatr,order[i],j)) for j in C]
        labels[order[i]] = ls
        try:        
            parents[order[i]] = C[0]
        except:
            parents[order[i]] = -1
    return labels, parents

def shortest_distance(AdjMatr,node1,node2):
    if node1 == node2:
        return np.inf
#        shortest distance 
    length = 1
    Matrix = AdjMatr.copy()
    PowerMatrix = np.eye(AdjMatr.shape[0])
    while(True):
        PowerMatrix = np.matmul(PowerMatrix,Matrix)
        if PowerMatrix[node1,node2] != 0:
            return length
        else:
            length += 1
        if length > AdjMatr.shape[0]:
            return np.inf

def is_parents(parents,node1,node2):
    parent1 = node1
    parent2 = node2
    while(True):
        parent1 = parents[parent1]
        if parent1 == node2:
            return (False,True)
        elif parent1 == -1:
            break
    while(True):
        parent2 = parents[parent2]
        if parent2 == node1:
            return (True,False)
        elif parent2 == -1:
            break
    return (False,False)

def s_distance_ad(labels,parents,u,v):
    dis = {}
    for key in labels:
        dis[key] = np.inf
    for label in labels[u]:
        dis[label[0]] = label[1]
    print('distance from child:',dis)
    c = parents[u]
    while(c != v):
        for label in labels[c]:
            if dis[c]+label[1]<dis[label[0]]:
                dis[label[0]] = dis[c]+label[1]
        c = parents[c]
    for label in labels[v]:
        if dis[label[0]]+label[1]<dis[v]:
            dis[v] = dis[label[0]]+label[1]
    return dis[v]

    





