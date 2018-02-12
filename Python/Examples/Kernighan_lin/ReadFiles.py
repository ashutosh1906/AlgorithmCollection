import Configuration_Custom
from kernighan_Lin_Compact import edge_list
def read_file_aschiip(edge_matrix,GRAPH_TYPE):
    file_pointer = open(Configuration_Custom.INPUT_FILE_NAME,'r+')
    read_file_undirected(file_pointer,edge_matrix)
    number_of_nodes = len(edge_matrix)
    for current_node in range(number_of_nodes):
        for adj_node in edge_matrix[current_node]:
            if current_node not in edge_matrix[adj_node]:
                edge_matrix[adj_node].append(current_node)

    for current_node in range(number_of_nodes):
        for adjacent_node in edge_matrix[current_node]:
            if adjacent_node < current_node:
                continue
            edge_list.append((current_node,adjacent_node))
    print("Number of Edges %s" % (len(edge_list)))

def read_file_undirected(file_pointer,edge_matrix):
    for line in file_pointer:
        line = line.replace('\n','')
        line = line.replace(' ','')
        if line == '':
            continue
        current_node = int(line[0:line.index('(')])-1
        edge_nodes = line[line.index('[')+1:line.index(']')].split(',')
        edge_matrix.append([])
        for node in edge_nodes:
            edge_matrix[current_node].append(int(node)-1)
    # Configuration_Custom.printAdjacentMatrix(edge_matrix)
