import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import math
import random
from ant_colony import AntColony

def load_vrp_data(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Find the <nodes> section
    nodes = []
    for node in root.findall(".//node"):
        node_id = int(node.get("id"))
        cx = float(node.find("cx").text)
        cy = float(node.find("cy").text)
        nodes.append({"id": node_id, "cx": cx, "cy": cy})

    # add demand per node
    for request in root.findall(".//request"):
        nodes[int(request.get("node"))-1].update({"demand":float(request.find("quantity").text)})
    
    return nodes


def calculate_distance_matrix(nodes):
    num_nodes = len(nodes)
    distance_matrix = [[0.0] * num_nodes for _ in range(num_nodes)]
    
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j:
                x1, y1 = nodes[i]["cx"], nodes[i]["cy"]
                x2, y2 = nodes[j]["cx"], nodes[j]["cy"]
                distance_matrix[i][j] = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            else:
                distance_matrix[i][j] = np.inf
    
    return distance_matrix


def plot(path, nodes):
    p = [int(i[0]) for i in path]
    p.append(path[-1][1]) # destination of last step

    points = [ nodes[i] for i in p]
    x = [i["cx"] for i in points]
    y = [i["cy"] for i in points]
    plt.plot(x,y)
    plt.show()


if __name__ == '__main__':
    nodes =  load_vrp_data("../../problem-instances/vehicle-routing/augerat-1995-set-a/A-n33-k05.xml")
#    print(nodes)
    distance_matrix = calculate_distance_matrix(nodes)
#    print(np.array(distance_matrix))
#    print(len(distance_matrix))
#    print(len(nodes))

#    print(nodes)
    demand = ( [  float(i["demand"]) if "demand" in i else 0 for i in sorted(nodes, key=lambda node: node["id"])] )
#    print(len(demand))
    ant_colony = AntColony(np.array(distance_matrix), 100, demand, 10, 1, 100, 0.95, alpha=1, beta=1)
    shortest_path = ant_colony.run()
    print("shorted_path: {}".format(shortest_path))
    plot(shortest_path[0], nodes)
