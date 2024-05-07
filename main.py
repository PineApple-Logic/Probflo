from Modules.NeticaPy3.netica import NeticaManager
import os
import json
from Modules.NeticaPy3.NeticaPy import State


# Path to the .neta file
NETWORK_FILE = 'Modules/Netica_Modules/Balule.neta'
JSON_FILE = 'conf/cas.json'
os.environ["NETICA_PASSWORD"] = "+RoseB/Jataware/310-7/4753"
CASE_FILE = 'Uploads/output.case'


def set_node_values(graph, data):
    for node_name, node_data in data.items():
        # Get the node by name
        node = graph.get_node_by_name(node_name)

        # Extract probabilities from node_data
        state_probabilities = list(node_data.values())

        # Assuming probabilities are represented as floats, we need to convert them to State objects
        # Create instances of State directly if provided by the Netica API
        state_probabilities_bn = [State(prob) for prob in state_probabilities]

        # Set the probabilities for the states of the node
        graph.set_node_probs(node, state_probabilities_bn)




def print_end_node_beliefs(graph):
    print("End Node Beliefs:")
    for node in graph.net_itr():
        if not node.GetFirstChild_bn():
            node_name = graph.get_node_name(node)
            print(f"Node: {node_name}")
            # Get the state names for the node from the JSON file
            state_names = graph.node_state_names[node_name]
            if state_names:
                # Iterate over the state names from the JSON file
                for state_name in state_names.keys():
                    # Get the belief for the state
                    belief = graph.get_node_belief(node, state_name)
                    print(f"  {belief:.4f}")  # Print only the belief
            print()


if __name__ == '__main__':
    # Initialize Netica manager
    netica_manager = NeticaManager()

    # Create a new network graph from the .neta file
    try:
        graph = netica_manager.new_graph(NETWORK_FILE)
    except FileNotFoundError:
        print(f"Failed to find network file: {NETWORK_FILE}")
        exit(1)

    # Load data from JSON file
    with open(JSON_FILE, 'r') as json_file:
        data = json.load(json_file)

    # Set node values based on the data from the JSON file
    set_node_values(graph, data)

    # Print beliefs of end nodes
    print_end_node_beliefs(graph)

    # Cleanup environment
    del netica_manager

