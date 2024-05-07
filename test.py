from Modules.NeticaPy3.netica import NeticaManager
import os
import json

# Path to the .neta file
NETWORK_FILE = 'Modules/Netica_Modules/Balule.neta'
JSON_FILE = 'conf/cas.json'
os.environ["NETICA_PASSWORD"] = "+RoseB/Jataware/310-7/4753"

def set_node_values(graph, data):
    for node_name, value in data.items():
        if isinstance(value, dict):
            for state_name, state_value in value.items():
                # Assuming the value in the JSON file is a dictionary containing state names and their values
                if state_name.isdigit():
                    state_index = int(state_name)
                else:
                    print(f"State '{state_name}' is not valid for node '{node_name}' in the network.")
                    continue
                graph.enter_finding(node_name, state_index)
        elif isinstance(value, str) or isinstance(value, int):
            # Assuming the value in the JSON file is either a string or an integer representing the state name or index
            if isinstance(value, str) and value.isdigit():
                value = int(value)
            graph.enter_finding(node_name, value)
        elif value is None:
            print(f"Node '{node_name}' has a None value in the JSON file.")
        else:
            print(f"Invalid value '{value}' for node '{node_name}' in the JSON file.")

def print_status_codes(graph, node_name):
    print(f"Status codes for node '{node_name}':")
    num_states = graph.get_num_node_states(node_name)
    for i in range(num_states):
        print(graph.get_node_state_name(node_name, i))


if __name__ == '__main__':
    # Initialize Netica manager
    netica_manager = NeticaManager()

    # Create a new network graph from the .neta file
    try:
        graph = netica_manager.new_graph(NETWORK_FILE)
    except FileNotFoundError:
        print(f"Failed to find network file: {NETWORK_FILE}")
        exit(1)

    # Get the node object for 'DISCHARGE_YR'
    discharge_node = graph.get_node('DISCHARGE_YR')

    if discharge_node is not None:
        print(f"Status codes for node 'DISCHARGE_YR':")
        for state_index in range(discharge_node.number_states()):
            state_name = discharge_node.state_names[state_index]
            print(f"State index: {state_index}, State name: {state_name}")
    else:
        print("Node 'DISCHARGE_YR' not found in the network.")

    # Cleanup environment
    del netica_manager
