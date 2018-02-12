import random,operator
import time
GRAPH_TYPE_A = 0
GRAPH_TYPE_B = 1
graph_node_region = {}
subgraph_list = [[] for i in range(2)]
node_external_internal_cost = [{} for i in range(2)]
unlocked_nodes = [{} for i in range(2)]
locked_nodes = []
number_of_nodes = 0
max_cost_nodes_values = [[-10000, -10000] for i in range(2)]
max_cost_nodes = [[-1,-1] for i in range(2)]
pairwise_gain = []
edge_list = []
boundary_nodes = [{} for i in range(2)]

def print_partitioned_graphs():
    print("Graph A %s" % (sorted(subgraph_list[0])))
    print("Graph B %s" % (sorted(subgraph_list[1])))

def validate_max_selection():
    print(">-----------------<\n")
    for i in range(2):
        # for node in node_external_internal_cost[i].keys():
        #     print("Current Node : %s" % (node))
        #     print("Benefit : %s" % (node_external_internal_cost[i][node]))
        print("%s ::: %s" % (i,sorted(node_external_internal_cost[i].items(), key=operator.itemgetter(1))))
        print("Max Nodes : %s"%(max_cost_nodes[i]))
        print("Max Nodes Values : %s" % (max_cost_nodes_values[i]))

def print_current_partitioned_graph():
    """Call this function to see the current partition of the graph"""
    print("In Summary")
    print("Graph A : %s\n Lenhth : %s" % (subgraph_list[0],len(subgraph_list[0])))
    print("Graph B : %s\n Lenhth : %s" % (subgraph_list[1],len(subgraph_list[1])))
    for node_index in graph_node_region.keys():
        print("%s : %s" % (node_index,graph_node_region[node_index]))

def print_estimation_nodes(adjacency_matrix):
    for nodes in range(number_of_nodes):
        print("Current Nodes %s --------------> "%(nodes))
        this_node_region = graph_node_region[nodes]
        internal_nodes = []
        external_nodes = []
        for adjacent_node in adjacency_matrix[nodes]:
            if graph_node_region[adjacent_node] == this_node_region:
                internal_nodes.append(adjacent_node)
            else:
                external_nodes.append(adjacent_node)
        print("Adjancey Matrix %s" % (adjacency_matrix[nodes]))
        print("Internal Nodes: %s" % (internal_nodes))
        print("External Nodes: %s" % (external_nodes))
        print("Cost %s" % (node_external_internal_cost[this_node_region][nodes]))


def generate_equal_random_partition_graphs(adjacency_matrix):
    global number_of_nodes
    ############################## Divide the Graph into two equal Subgraphs #############
    for index in range(number_of_nodes):
        # print("Index %s" % (index))
        if (index <= (number_of_nodes / 2)):
            while (True):
                node_index = random.randint(0, number_of_nodes - 1)
                if node_index not in graph_node_region.keys():
                    graph_node_region[node_index] = GRAPH_TYPE_A
                    subgraph_list[0].append(node_index)
                    break
        else:
            while (True):
                node_index = random.randint(0, number_of_nodes - 1)
                if node_index not in graph_node_region.keys():
                    graph_node_region[node_index] = GRAPH_TYPE_B
                    subgraph_list[1].append(node_index)
                    break
                    ############################## Divide the Graph into two equal Subgraphs #############

def initial_estimate_node_cost(adjacency_matrix):
    global number_of_nodes
    # print("Size of the graph %s" % (number_of_nodes))
    print("Cost List %s" % (node_external_internal_cost))
    for current_node_index in range(number_of_nodes):
        this_node_region = graph_node_region[current_node_index]
        node_external_internal_cost[this_node_region][current_node_index] = 0
        unlocked_nodes[this_node_region][current_node_index] = 1
        for adjacent_node in adjacency_matrix[current_node_index]:
            if graph_node_region[adjacent_node] == this_node_region:
                node_external_internal_cost[this_node_region][current_node_index] -= 1
            else:
                node_external_internal_cost[this_node_region][current_node_index] += 1

def calculate_max_gain_nodes(adjacency_matrix):
    for i in range(2):
        iter_index = 0
        for current_node in unlocked_nodes[i].keys():
            if iter_index == 0:
                max_cost_nodes_values[i][0] = node_external_internal_cost[i][current_node]
                max_cost_nodes[i][0] = current_node
                iter_index += 1
                continue
            if iter_index == 1:
                max_cost_nodes_values[i][1] = node_external_internal_cost[i][current_node]
                max_cost_nodes[i][1] = current_node
            if max_cost_nodes_values[i][0] < node_external_internal_cost[i][current_node]:
                max_cost_nodes_values[i][1] = max_cost_nodes_values[i][0]
                max_cost_nodes[i][1] = max_cost_nodes[i][0]
                max_cost_nodes_values[i][0] = node_external_internal_cost[i][current_node]
                max_cost_nodes[i][0] = current_node
            elif max_cost_nodes_values[i][1] < node_external_internal_cost[i][current_node]:
                max_cost_nodes_values[i][1] = node_external_internal_cost[i][current_node]
                max_cost_nodes[i][1] = current_node
            iter_index += 1

    pair_locked_nodes = [-1,-1]
    max_gain = -number_of_nodes-number_of_nodes
    for a_node in max_cost_nodes[0]:
        for b_node in max_cost_nodes[1]:
            current_gain = node_external_internal_cost[0][a_node]+node_external_internal_cost[1][b_node]
            # print("Node A: %s Node B:%s Values: (%s,%s)"%(a_node,b_node, node_external_internal_cost[0][a_node],
            #                                               node_external_internal_cost[1][b_node]))
            if b_node in adjacency_matrix[a_node]:
                # print("%s in Adjacency %s of %s" % (b_node,adjacency_matrix[a_node],a_node))
                current_gain -= 2
            if max_gain < current_gain:
                max_gain = current_gain
                pair_locked_nodes[0] = a_node
                pair_locked_nodes[1] = b_node
    locked_nodes.append(pair_locked_nodes)
    del unlocked_nodes[GRAPH_TYPE_A][pair_locked_nodes[0]]
    del unlocked_nodes[GRAPH_TYPE_B][pair_locked_nodes[1]]
    if len(pairwise_gain) == 0:
        pairwise_gain.append(max_gain)
    else:
        pairwise_gain.append(pairwise_gain[len(pairwise_gain)-1] + max_gain)
    return max_gain

def update_cost_other_nodes(locked_nodes_iteration,adjacency_matrix):
    # print("Currently Locked Nodes %s" % (locked_nodes_iteration))
    for i in range(2):
        for current_node in unlocked_nodes[i].keys():
            change_value = 0
            if locked_nodes_iteration[0] in adjacency_matrix[current_node]:
                change_value += 2
            if locked_nodes_iteration[1] in adjacency_matrix[current_node]:
                change_value -= 2
            node_external_internal_cost[i][current_node] += pow(-1,i)*change_value

def partitioned_graphs():
    for i in range(2):
        del subgraph_list[i][:]

def count_cut_edge(adjacency_matrix):
    cut_edge = 0
    for edge in edge_list:
        if graph_node_region[edge[0]] != graph_node_region[edge[1]]:
            cut_edge += 1
    print("(*_*)(*_*)(*_*)(*_*) Number of Cut Edges %s (*_*)(*_*)(*_*)(*_*)" % (cut_edge))

def createBoundaryNodes():
    for edge in edge_list:
        if graph_node_region[edge[0]] != graph_node_region[edge[1]]:
            boundary_nodes[graph_node_region[edge[0]]][edge[0]] = 1
            boundary_nodes[graph_node_region[edge[1]]][edge[1]] = 1
    # print("(*_*)(*_*)(*_*)(*_*) Bounday Nodes %s : %s  (*_*)(*_*)(*_*)(*_*)" % (len(boundary_nodes[GRAPH_TYPE_A]),boundary_nodes[GRAPH_TYPE_A]))
    # print("(*_*)(*_*)(*_*)(*_*) Bounday Nodes %s : %s  (*_*)(*_*)(*_*)(*_*)" % (len(boundary_nodes[GRAPH_TYPE_B]),boundary_nodes[GRAPH_TYPE_B]))

def init_env():
    del locked_nodes[:]
    del pairwise_gain[:]
    for i in range(2):
        node_external_internal_cost[i].clear()
        unlocked_nodes[i].clear()

def graph_partitioner(adjacency_matrix):
    global number_of_nodes
    number_of_nodes = len(adjacency_matrix)
    print("Size of the graph %s" % (number_of_nodes))
    generate_equal_random_partition_graphs(adjacency_matrix)
    # print_current_partitioned_graph()
    ####################################### End of the cost for the nodes ###################################

    ########################################### Select the max nodes ####################################
    outer_iter_index = 0
    start_time = time.time()
    while(True):
        print("\n\nIteration Number %s" % (outer_iter_index))
        g_max = -1
        ####################################### Create the cost for the nodes ###################################
        init_env()
        initial_estimate_node_cost(adjacency_matrix)
        for i in range(int(number_of_nodes/2)):
            gain = calculate_max_gain_nodes(adjacency_matrix)
            # validate_max_selection()
            # print("Current Locked Nodes %s"%(locked_nodes[-1]))
            update_cost_other_nodes(locked_nodes[-1],adjacency_matrix)
            ########################################### End of Selection of the max nodes ####################################

        ############################################# Find the maximum K #####################################################
        # print("Locked Gain : %s" % (pairwise_gain))
        g_max = pairwise_gain[0]
        max_k = 0
        for i in range(len(pairwise_gain)):
            if g_max < pairwise_gain[i]:
                g_max = pairwise_gain[i]
                max_k = i
        ############################################## End of finding of the maximum K #######################################

        print("G Max is %s Maxk K %s" % (g_max,max_k))
        if g_max <= 0:
            break

        print("Before Partition")
        count_cut_edge(adjacency_matrix)
        ############################################# Change the Graph Partition #########################################
        for i in range(max_k+1):
            # print("Iteration %s : %s" % (i,locked_nodes[i]))
            for current_node in locked_nodes[i]:
                # print("Node %s\nPrevious Partition %s" % (current_node,graph_node_region[current_node]))
                graph_node_region[current_node] ^= 1
                # print("Current Partition %s" % (graph_node_region[current_node]))
        ############################################# End of Change of the Graph Partition ###############################

        ############################################ Check the Graphs ###################################################
        # print_partitioned_graphs()

        partitioned_graphs()
        for node in graph_node_region.keys():
            subgraph_list[graph_node_region[node]].append(node)
        # print_partitioned_graphs()
        print("After Partition")
        count_cut_edge(adjacency_matrix)
        outer_iter_index += 1
        ############################################ End of checking the Graphs #########################################
    print("Duration %s" % (time.time()-start_time))
    createBoundaryNodes()
    return {'subgraph':subgraph_list,'node_region':graph_node_region,'bounday_nodes':boundary_nodes}

