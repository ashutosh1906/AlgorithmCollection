DIRECTED_GRAPH = 1
UNIDIRECTED_GRAPH = 0
INPUT_FILE_NAME = 'Topology1.txt'
######################## The threshold for reachability in the other graphs ##############
DEPTH_THRESHOLD = 80
############################# Output File Name ##########################################
GRAPH_NAME_A = 'graph_A.txt'
GRAPH_NAME_B = 'graph_B.txt'

def printAdjacentMatrix(edge_matrix):
    for node in range(len(edge_matrix)):
        print("%s : %s" % (node,edge_matrix[node]))