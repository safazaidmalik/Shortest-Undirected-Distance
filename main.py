import numpy as np
import matplotlib.pyplot as plt
import utils
import pickle
import glob
import time
import os
#print("hello")

# small input 1
#nodes = 4
#AdjMatr = np.array(                      
#           [[0,1,0,0],
#           [1,0,1,1],
#           [0,1,0,1],
#           [0,1,1,0]]
#                                )      
#np.savetxt('query_sample0.csv',AdjMatr,delimiter=',',fmt='%s')
#                                
#small input 2
#                   
#nodes = 8
#AdjMatr = np.array(
#           [[0,1,1,0,0,1,0,0],
#           [1,0,1,1,1,0,1,0],
#           [1,1,0,1,0,0,0,0],
#           [0,1,1,0,1,0,0,0],
#           [0,1,0,1,0,0,0,1],
#           [1,0,0,0,0,0,0,0],
#           [0,1,0,0,0,0,0,0],
#           [0,0,0,0,1,0,0,0]]
#                                )
#
#
#small input 3
#nodes = 8
#AdjMatr = np.array(
#          [[0,0,0,1,0,0,1,1,0,1],
#           [0,0,1,1,1,0,0,0,1,0],
#           [0,1,0,0,0,0,0,1,1,1],
#           [1,1,0,0,1,0,1,0,1,1],
#           [0,1,0,0,0,1,1,0,0,0],
#           [0,0,0,0,1,0,0,0,1,0],
#           [1,0,0,1,1,0,0,0,0,0],
#           [1,0,1,0,0,0,0,0,1,1],
#           [0,1,1,1,0,1,0,1,0,1],
#           [1,0,1,1,0,0,0,1,1,0]]
#                                )
#np.savetxt('query_sample1.csv',AdjMatr,delimiter=',',fmt='%s')
#
#
#nodenums = [50,100,200,400,700,1000,2000,3000,4000,5000]                                              
#for i in range(10):
#    nodes = nodenums[i]
#    AdjMatr = np.random.randint(0,2,(nodes,nodes))
#    AdjMatr = np.triu(AdjMatr) + np.triu(AdjMatr).T

#
#
#Fix this 
#    for j in range(nodes):
#        AdjMatr[j][j] =0
#    np.savetxt(f'random_sample{i}.csv',AdjMatr,delimiter=',',fmt='%s')
#
filenames = glob.glob('*.csv') 
filenames = sorted(filenames)
nodes = [8,4,10,50,100,200,400]
for i in range(len(filenames)):
    print(i,filenames[i], nodes[i])



times = []
file_id = int(input('Choose file number.'))
filenames = [filenames[file_id]]
nodes = nodes[file_id]
for fil in filenames:
    a = time.time()
    print(fil)
    print('Time Start:')
    AdjMatr = np.loadtxt(fil,delimiter=',')
#if True:
    print('AdjMatr:')
    print(AdjMatr, '\n')
    elim_path = f'Data/elim_{fil}'
    added_path = f'Data/added_{fil}'    
    if os.path.exists(elim_path[:-3]+'pickle'):
        print('elimination order file exists')
        elimination_order = pickle.load(open(elim_path[:-3]+'pickle','rb'))
        added_connections = pickle.load(open(added_path[:-3]+'pickle','rb'))
        print('elimination order loaded')
    else:
        elimination_order,added_connections = utils.get_elimination_order(AdjMatr)
        added_connections = np.array(added_connections).astype(int)
        elimination_order = np.array(elimination_order).astype(int)
        pickle.dump(elimination_order,open(elim_path[:-3]+'pickle','wb'))
        pickle.dump(added_connections,open(added_path[:-3]+'pickle','wb'))
    print('elimination_order')
    print(elimination_order, '\n')
    labels_path = f'Data/labels_{fil}'
    parents_path = f'Data/parents_{fil}'    
    if os.path.exists(labels_path[:-3]+'pickle'):
        print('labels file exists')
        labels = pickle.load(open(labels_path[:-3]+'pickle','rb'))
        parents = pickle.load(open(parents_path[:-3]+'pickle','rb'))
        print('labels,parents loaded')

    else:
        print('labels file does not exist')
        fill_in_graph = utils.get_fill_in_graph(AdjMatr,added_connections)
        labels, parents = utils.get_labelling(elimination_order,fill_in_graph)
        pickle.dump(labels,open(labels_path[:-3]+'pickle','wb'))
        pickle.dump(parents,open(parents_path[:-3]+'pickle','wb'))
#    print('labels')
#    print(labels,'\n')
    print('parents')
    print(parents, '\n')
    while(True):
        node1 = int(input('Enter the first node ID.'))
        node2 = int(input('Enter the second node ID.'))
        parent_status = utils.is_parents(parents,node1,node2)
        if parent_status[0]==True:
            break
        if parent_status[1]==True:
            break
        print('Sorry. Try Again! No ancestry found. ', '\n')
    if parent_status[0]==True:
        print('Ancestor:',node1, ' Child:',node2)
        dis_v = utils.s_distance_ad(labels,parents,node2,node1)
    elif parent_status[1]==True:
        print('Ancestor:',node2, ' Child:',node1)
        dis_v = utils.s_distance_ad(labels,parents,node1,node2)
    print('Distance from u to v:', dis_v)
    end = time.time()
    print('Time taken for program = ', end - a)

    times.append(end-a)

img = plt.imread('Figure_1.png')
plt.imshow(img)
plt.axis('off')
#plt.plot(nodes,times)
#plt.scatter(nodes,times)
plt.show()
