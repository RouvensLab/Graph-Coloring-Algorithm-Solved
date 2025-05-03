#This Program should show that the COL problem is NP-Complete. So I made a polynomial time efficient algorithm to solve the problem.
# How to run the program over the command line:
# python COL_Problems.py --time_efficiency
# python COL_Problems.py --example

import argparse
import networkx as nx
import matplotlib.pyplot as plt
import copy
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import time

class GraphColoring:
    def __init__(self, n_nodes=8, n_edges=0.01):
        #generating a  graph G that can be colored with 3 colors minimum.
        #generate a random graph
        self.G = nx.random_geometric_graph(n_nodes, n_edges)
        self.pos = nx.spring_layout(self.G, seed=3113794652)  # positions for all nodes
        self.generate_node_connection_structure(self.G)

    def paste_graph(self, endges_list:list):
        #empty graph
        self.G = nx.Graph()
        for edge_connection in endges_list:
            #add endges and nodes to the graph
            self.G.add_edge(edge_connection[0], edge_connection[1])

        self.pos = nx.spring_layout(self.G, seed=3113794652)  # positions for all nodes
        self.generate_node_connection_structure(self.G)

    

    def generate_node_connection_structure(self, G: nx.Graph):
        self.n_nodes = len(G.nodes)
        # convert the graph to a dictionary like self.graph_connections = {1: [2, 3, 4, 5], 2: [1, 3, 4], 3: [1, 4], 4: [1], 5: [6, 7, 8], 6: [5, 7, 8], 7: [5, 8], 8: [5]}
        self.graph_connections = {}
        print(G.edges)
        for edge in G.edges:
            if edge[0] in self.graph_connections.keys():
                self.graph_connections[edge[0]].append(edge[1])
            else:
                self.graph_connections[edge[0]] = [edge[1]]

            if edge[1] in self.graph_connections.keys():
                self.graph_connections[edge[1]].append(edge[0])
            else:
                self.graph_connections[edge[1]] = [edge[0]]
        #check if all the nodes are contained in the graph_connections
        for node_id in G.nodes:
            if node_id not in self.graph_connections.keys():
                self.graph_connections[node_id] = []
        
        self.colored_graph = {}
        for node_id, node_value in self.graph_connections.items():
            self.colored_graph[node_id] = {"color": 0, "connections": node_value}
        return self.colored_graph

    def generate_graph(self, graph_connections, color_map_type=None):
        #self.G = nx.Graph()
        self.G.clear()

        nodes_ids = []
        nodes_colors = []


        # Edgelist like [(4, 5), (5, 6), (6, 7), (7, 4)]
        edgeslist = []
        for node_id, node_value in graph_connections.items():
            # Give a color to the node_id
            nodes_ids.append(node_id)
            nodes_colors.append(node_value['color'])
            for connection_id in node_value["connections"]:
                edgeslist.append((node_id, connection_id))
        # print(edgeslist)
        # print(nodes_ids)
        
        if color_map_type == "complementary":
            max_node_color = max(nodes_colors)+2
            colormap = self.generate_colors(max_node_color)
            #convert the colors given by a integer to a color with the colormap
            nodes_colors = [colormap[color] for color in nodes_colors]
        else:
            colormap = self.generate_colors(self.n_nodes)
            nodes_colors = [colormap[color] for color in nodes_colors]

        
        self.G.add_nodes_from(nodes_ids)
        self.G.add_edges_from(edgeslist)
        
        pos = nx.spring_layout(self.G, seed=3113794652)  # positions for all nodes

        nx.draw_networkx_nodes(self.G, pos=pos, nodelist=nodes_ids, node_color=nodes_colors)
        nx.draw_networkx_edges(
            self.G,
            pos,
            edgelist=edgeslist,
        )
        #show the ids of the nodes
        nx.draw_networkx_labels(self.G, pos, font_size=10, font_family="sans-serif")
        return self.G

    
    def generate_colors(self, n):
        # Create a colormap that goes from Red to Green to Blue
        colormap = cm.get_cmap('hsv', n)
        
        # Generate n colors and convert them to hexadecimal format
        colors = [mcolors.to_hex(colormap(i)) for i in range(n)]
        
        return colors
    
    def COLN(self, show_graph=True):
        #function to check if the graph is 3-colorable
        #colors the nodes (with the most connections first) connected nodes (with new color) until there are no nodes left.
        #so first sort the nodes by the number of connections
        sorted_nodes = sorted(self.colored_graph.keys(), key=lambda x: len(self.colored_graph[x]["connections"]), reverse=True)
        all_colored_ids = copy.deepcopy(sorted_nodes)
        print(sorted_nodes)#sorted nodes is linked with the colored graph
        

        in_progress = True
        time_eff_num_iter = 0
        num_iter = 0
        while in_progress:
            #1. Step
            all_major_ids, all_colored_ids, num2_iter = self.COL2(all_colored_ids, color=num_iter+1)
            all_colored_ids = list(all_colored_ids.keys())

            #2. Step
            #remove all the major_ids nodes from the sorted_nodes
            for major_id in all_major_ids.keys():
                sorted_nodes.remove(major_id)

            if show_graph:
                #generate the graph
                G = self.generate_graph(graph_connections=self.colored_graph)
                plt.show()
                print("Sorted Nodes:", sorted_nodes)

            #check if there are no nodes left
            if len(sorted_nodes) == 0:
                in_progress = False
            time_eff_num_iter += num2_iter
            num_iter += 1
        return num_iter, time_eff_num_iter



    def COL2(self, sorted_nodes_list, color=0):
        #1. Step
        num_iter = 0
        all_colored_ids = {}
        all_major_ids = {}
        for node_id in sorted_nodes_list:
            node_value = self.colored_graph[node_id]
            #check if the node contains a colored connected node
            if node_id in all_colored_ids.keys():
                continue
            else:
                #color the connected nodes
                all_major_ids[node_id] = True
                for connected_node_id in node_value["connections"]:
                    if connected_node_id in sorted_nodes_list:
                        self.colored_graph[connected_node_id]["color"] = color
                        #add the connected nodes to the list of colored nodes
                        all_colored_ids[connected_node_id] = True
                    num_iter += 1

        #show the colored graph
        #print(sorted_nodes_list)
        return all_major_ids, all_colored_ids, num_iter
    
    def quicksolve(self, graph: nx.Graph = None, show_graph=True):
        """funktion to solve the graph coloring problem
        returns the number of iterations and the time efficiency
        show_graph: shows the graph when True
        """
        if graph is not None:
            self.G = graph

        self.pos = nx.spring_layout(self.G, seed=3113794652)  # positions for all nodes
        self.generate_node_connection_structure(self.G)

        self.n_nodes = len(self.G.nodes)
        num_iter, time_eff_num_iter = self.COLN(show_graph=False)
        if show_graph:
            self.generate_graph(graph_connections=self.colored_graph, color_map_type="complementary")
            print(f"Number of Colors: {num_iter}")
            print(f"Time Efficiency: {time_eff_num_iter}")
            plt.show()

        return num_iter, time_eff_num_iter

        

    
    def measure_time_complexity(self, max_nodes=50, step=5):
        n_values = []
        time_eff_values = []
        time_eff_list = []

        for n in range(5, max_nodes + 1, step):
            self.__init__(n_nodes=n, n_edges=0.5)
            start_time = time.time()
            _, time_eff_num_iter = self.COLN(show_graph=False)
            end_time = time.time()
            time_eff = end_time - start_time
            n_values.append(n)
            time_eff_list.append(time_eff)
            time_eff_values.append(time_eff_num_iter)

            print(f"n: {n}, time_eff_num_iter: {time_eff_num_iter}, time_eff: {time_eff}")

        #plt.plot(n_values, time_eff_values, marker='o')
        #plot the real time efficiency
        plt.plot(n_values, time_eff_list, marker='o')
        plt.xlabel('Number of Nodes (n)')
        plt.ylabel('Time Efficiency (time_eff_num_iter)')
        plt.title('Time Complexity of Graph Coloring Algorithm')
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Graph Coloring Algorithm")
    parser.add_argument('--time_efficiency', action='store_true', help="Run the time efficiency test")
    parser.add_argument('--example', action='store_true', help="Show an example graph coloring")

    args = parser.parse_args()

    GC = GraphColoring(n_nodes=10, n_edges=0.5)#n_nodes = number of nodes, n_edges = number of connections in percentage

    # costom_edges_graph = [
    #     (1,4),
    #     (1,2),
    #     (1, 3),
    #     (1, 6),
    #     (1,7),
    #     (3, 4),
    #     (4,7),
    #     (3, 6),
    #     (6, 7),
    #     (4, 5),
    #     (2, 5),
    #     (4, 8),
    #     (5, 8),
    #     (7, 5),
    #     (6, 9),
    #     (9,7),
    #     (10, 9),
    #     (5, 10),
    #     (10,8),
    #     (4, 6),
    #     (3, 7)
    # ]
    # GC.paste_graph(costom_edges_graph)
    #show the colored graph
    #print(GC.COLN(show_graph=True))
    print(GC.quicksolve(show_graph=True))

    # if args.time_efficiency:
    #     GC.measure_time_complexity(max_nodes=300, step=5)
    # elif args.example:
    #     #shows the seps of the graph coloring (every step a new color is used, except the last step it just shows the same graph)
    #     print(GC.COLN(show_graph=True))
    # else:
    #     print(GC.quicksolve(show_graph=True))
    #     print("Please specify --time_efficiency or --example")
