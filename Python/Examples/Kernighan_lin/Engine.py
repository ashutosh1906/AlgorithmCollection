import ReadFiles
import Configuration_Custom
import kernighan_Lin_Compact
NUMBER_OF_SUBGRAPH = 2
subgraph_adjacency_matrix = [{} for i in range(NUMBER_OF_SUBGRAPH)]
other_graph_adjacency_matrix = [{} for i in range(NUMBER_OF_SUBGRAPH)]
other_graph_reachability = [[] for i in range(2)]

def print_new_adjacency_matrix():
    for i in range(NUMBER_OF_SUBGRAPH):
        print("Region %s" % (i))
        for current_node in subgraph_adjacency_matrix[i].keys():
            print("Current Node %s : %s" % (current_node,subgraph_adjacency_matrix[i][current_node]))

def prepare_adjacency_matrix_for_internal(adjacency_matrix,graph_node_region):
    # print("Graph Node Region %s" % (graph_node_region))
    number_of_nodes = len(adjacency_matrix)
    for current_node in range(number_of_nodes):
        current_node_region = graph_node_region[current_node]
        subgraph_adjacency_matrix[current_node_region][current_node] = []
        other_graph_adjacency_matrix[current_node_region][current_node] = []
        for adjacent_node in adjacency_matrix[current_node]:
            if current_node_region != graph_node_region[adjacent_node]:
                other_graph_adjacency_matrix[current_node_region][current_node].append(adjacent_node)
                continue
            subgraph_adjacency_matrix[current_node_region][current_node].append(adjacent_node)

if __name__=='__main__':
    ########################## Declare the edge matrix ###########
    adjacent_matrix = []
    ########################## End of the declaration ############

    ################## Read The Files ############################
    ReadFiles.read_file_aschiip(adjacent_matrix,Configuration_Custom.UNIDIRECTED_GRAPH)
    ################# End of read of the files ###################

    #################### Call the Graph Partition Algorithm ###################
    partition_graphs = kernighan_Lin_Compact.graph_partitioner(adjacent_matrix)
   
    #################### End of Call the Graph Partition Algorithm #########

    ############################# Write In The File ###############################################################
    file_write = []
    file_write.append(open(Configuration_Custom.GRAPH_NAME_A,'w'))
    file_write.append(open(Configuration_Custom.GRAPH_NAME_B,'w'))
    for file_index in range(2):
        for current_node in partition_graphs['subgraph'][file_index]:
            write_line = ""
            write_line += "%s (%s) [" % (current_node+1,file_index)
            for node_index in range(len(adjacent_matrix[current_node])-1):
                write_line += "%s, " % (adjacent_matrix[current_node][node_index]+1)
            write_line += "%s]\n" % (adjacent_matrix[current_node][len(adjacent_matrix[current_node])-1]+1)
            file_write[file_index].write(write_line)
        
        file_write[file_index].close()
    ############################# Write In The File ###############################################################
