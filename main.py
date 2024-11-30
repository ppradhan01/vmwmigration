import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt
import nncp
import nad
import nmstate


class Node:
    def __init__(self, node_id, name, node_type, text):
        self.id = node_id
        self.name = name
        self.type = node_type
        self.text = text

    def __repr__(self):
        return f"Node(id={self.id}, name={self.name}, type={self.type}, text={self.text})"

class Edge:
    def __init__(self, edge_type, from_node, to_node):
        self.type = edge_type
        self.from_node = from_node
        self.to_node = to_node

    def __repr__(self):
        return f"Edge(type={self.type}, from={self.from_node}, to={self.to_node})"

class Graph:
    def __init__(self):
        self.nodes = {}  # Dictionary to store nodes by their ID
        self.edges = []  # List to store edges

    def add_node(self, node_id, name, node_type, text):
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id, name, node_type, text)

    def add_edge(self, edge_type, from_node, to_node):
        if from_node in self.nodes and to_node in self.nodes:
            self.edges.append(Edge(edge_type, from_node, to_node))

    def visualize(self):
        # Create a NetworkX graph
        G = nx.DiGraph()

        # Add nodes with labels
        for node_id, node in self.nodes.items():
            G.add_node(node_id, label=node.name, text=node.text, type=node.type)

        # Add edges with labels
        for edge in self.edges:
            G.add_edge(edge.from_node, edge.to_node, label=edge.type)

        # Get node labels for display
        node_labels = {node_id: f"{node.name}\n({node.text})" for node_id, node in self.nodes.items()}
        
        # Get edge labels for display
        edge_labels = {(edge.from_node, edge.to_node): edge.type for edge in self.edges}

        # Draw the graph
        pos = nx.spring_layout(G)  # Layout for positioning nodes
        plt.figure(figsize=(10, 8))

        nx.draw(
            G, pos, with_labels=True, labels=node_labels, node_color="lightblue", node_size=3000, font_size=10
        )
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")

        # Display the graph
        plt.title("Graph Visualization")
        plt.show()

    def walk_and_process(self, start_node_id):
        visited = set()

        # generate one global nmstate config
        self.generate_NMState("eth0","eth1")

        def recursive_walk(node_id):
            if node_id in visited:
                return
            visited.add(node_id)
            print("calling recursive_walk on "+node_id)

            node = self.nodes[node_id]


            # If node type is "vSwitch", call generated_NNCP()
            if node.type == "vSwitch":
                print(f"Processing vSwitch : {node.name}")
                vlans = []
                # look for connected portgroups/vlans
                for edge in self.edges:
                    if edge.from_node == node_id :
                        if self.nodes[edge.to_node].type == "PortGroup" :
                            # aggregate vlans to generate 1 nncp
                            vlans.append(self.nodes[edge.to_node].text)
                            self.generate_NAD(self.nodes[edge.to_node].text)
                self.generate_NNCP(vlans)

                # Process all "CONNECTS" edges from this node - use this if we need to do something per VM
                # for edge in self.edges:
                #    if edge.from_node == node_id and edge.type == "CONNECTS":
                #        connected_node = self.nodes[edge.to_node]
                #        print(f"Processing connected Node: {connected_node.name}")

            # Recurse into connected nodes
            for edge in self.edges:
                if edge.from_node == node_id:
                    recursive_walk(edge.to_node)

        # Start the recursive walk
        recursive_walk(start_node_id)

    # Placeholder function for NNCP generation
    def generate_NMState(self,intf0,intf1):
        print("Generating NMState")
        nmstate.replace_interfaces_in_yaml("./nmstate-config-template.yaml", "./nmstate-config.yaml", intf0, intf1)

    # Placeholder function for NNCP generation
    def generate_NNCP(self, vlans):
        print("Generating NNCP for "+str(vlans))
        nncp.replace_vlan_ids_in_yaml("./nncp-template.yaml", "./nncp.yaml", vlans)

    # Placeholder function for NAD generation
    def generate_NAD(self, text):
        print("Generating NAD for "+text)
        nad.replace_vlan_id_in_yaml("./nad-template.yaml", "./nad-"+text+".yaml", text)


    def __repr__(self):
        return f"Graph(nodes={list(self.nodes.values())}, edges={self.edges})"

# Parse the XML file and populate the Graph
def parse_xml_to_graph(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    graph = Graph()

    # Parse nodes
    for node in root.find("Nodes"):
        graph.add_node(
            node_id=node.attrib["id"],
            name=node.attrib["name"],
            node_type=node.attrib["type"],
            text=node.attrib["text"]
        )

    # Parse relationships
    for rel in root.find("Relationships"):
        graph.add_edge(
            edge_type=rel.attrib["type"],
            from_node=rel.attrib["from"],
            to_node=rel.attrib["to"]
        )

    return graph

# Example usage
if __name__ == "__main__":
    # Path to the XML file
    file_path = "./file.xml"

    # Parse the XML and create the graph
    graph = parse_xml_to_graph(file_path)

    # Print the graph representation
    print(graph)

    # Walk the graph and process nodes
    start_node_id = "1"  # Change this to the starting node ID as required
    graph.walk_and_process(start_node_id)

    # Visualize the graph
    graph.visualize()
