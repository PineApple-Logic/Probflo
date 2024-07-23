# In run.py
from Modules.Netica_Modules.netica import NeticaManager, logger
from Modules.NeticaPy3.NeticaPy import Netica, NewNode as NeticaNode
import os
import json

BASE_DIR = os.getcwd()

# Path to the .neta file
NETWORK_FILE = './Modules/Netica_Modules/Balule.neta'
os.environ["NETICA_PASSWORD"] = "+RoseB/Jataware/310-7/4753"
N = Netica()


def set_node_values(graph, data):
    for node_name, node_data in data.items():
        try:
            if graph.get_node_by_name(node_name) is None:
                logger.warning(f"Warning: Node '{node_name}' not found in the network.")
                continue
            else:
                node = graph.get_node_by_name(node_name)  # Get the node object from the graph
                node_states = graph.ParentNodeStates(
                    node_name.encode('utf-8'))  # Get the state names for the nodes in the network

            # Set the probabilities for the node from the JSON file
            graph.set_node_probabilities(node, node_name.encode('utf-8'), node_states, node_data)

        except KeyError:
            logger.warning(f"Warning: Node '{node_name}' not found in the network.")
        except Exception as e:
            logger.error(f"Error setting values for node '{node_name}': {e}")


def convert_strings_to_floats(input_array):
    output_array = []
    for element in input_array:
        converted_float = float(element)
        output_array.append(converted_float)
    return output_array


def collect_end_node_beliefs(graph):
    end_node_beliefs = {}
    for node in graph.net_itr():
        if N.LengthNodeList_bn(N.GetNodeChildren_bn(node)) == 0:  # Checking if the node has no children
            node_name = graph.get_node_name(node)
            node_beliefs = {}
            # Get the state names for the node from the JSON file
            state_names = graph.node_state_names.get(node_name, {})
            if state_names:
                # Iterate over the state names from the JSON file
                for state_name in state_names.keys():
                    # Get the belief for the state
                    try:
                        belief = graph.get_node_belief(node, state_name)
                        node_beliefs[state_name] = belief
                    except Exception as e:
                        print(f"Error getting belief for state '{state_name}' of node '{node_name}': {e}")
            end_node_beliefs[node_name] = node_beliefs
    return end_node_beliefs


def save_beliefs_to_json(end_node_beliefs, output_file):
    try:
        with open(output_file, 'w') as file:
            json.dump(end_node_beliefs, file, indent=4)
        print(f"Beliefs saved to {output_file}")
    except IOError as e:
        logger.error(f"Error saving beliefs to JSON file: {e}")

def print_end_node_beliefs(graph):
    print("End Node Beliefs:")
    for node in graph.net_itr():
        if N.LengthNodeList_bn(N.GetNodeChildren_bn(node)) == 0:  # Checking if the node has no children
            node_name = graph.get_node_name(node)
            print(f"Node: {node_name}")
            # Get the state names for the node from the JSON file
            state_names = graph.node_state_names.get(node_name, {})
            if state_names:
                # Iterate over the state names from the JSON file
                for state_name in state_names.keys():
                    # Get the belief for the state
                    try:
                        belief = graph.get_node_belief(node, state_name)
                        print(f"  {state_name}: {belief:.4f}")  # Print the state name and belief
                    except Exception as e:
                        print(f"Error getting belief for state '{state_name}' of node '{node_name}': {e}")
            print()


def main(JSON_FILE, output_json_file):
    # Initialize Netica manager
    netica_manager = NeticaManager()

    # Create a new network graph from the .neta file
    try:
        graph = netica_manager.new_graph(NETWORK_FILE)
    except FileNotFoundError:
        logger.error(f"Failed to find network file: {NETWORK_FILE}")
        exit(1)
    except Exception as e:
        logger.error(f"Error creating network graph: {e}")
        exit(1)

    # Load data from JSON file
    try:
        with open(JSON_FILE, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        logger.error(f"Failed to find JSON file: {JSON_FILE}")
        exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON file: {e}")
        exit(1)

    # Set node values based on the data from the JSON file
    set_node_values(graph, data)

    # Collect beliefs of end nodes and save them to a JSON file
    end_node_beliefs = collect_end_node_beliefs(graph)
    save_beliefs_to_json(end_node_beliefs, output_json_file)

    print_end_node_beliefs(graph)

    # Cleanup environment
    os.remove(f'{JSON_FILE}')
    del netica_manager


if __name__ == '__main__':
    os.chdir('../../')
    main('./conf/case (2).json', './conf/end_case (2).json')
