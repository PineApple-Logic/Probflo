from Modules.NeticaPy3.netica import NeticaManager
from Modules.NeticaPy3.NeticaPy import NewNode
import os

# Initialize Netica
os.environ["NETICA_PASSWORD"] = "+RoseB/Jataware/310-7/4753"

if __name__ == '__main__':
    # Initialize Netica manager
    netica_manager = NeticaManager()

    # Create a new environment
    env = netica_manager.env

    # Create a new network graph (changed from new_network to new_graph)
    graph = netica_manager.new_graph("SimpleNetwork")

    # Add a node without any parents
    node = NewNode(b"SimpleNode", 0, graph.net)

    # Set the states for the node
    netica_manager.set_node_state_names(node, b"State1, State2")

    # Set probabilities for the states of the node (arbitrary values)
    netica_manager.set_node_probs(node, [0.6, 0.4])

    # Print the probabilities before changing
    print("Probabilities before changing:")
    for i in range(netica_manager.get_node_number_states(node)):
        print(f"State{i + 1}: {netica_manager.get_node_probs(node)[i]}")

    # Attempt to change the probabilities for the states of the node
    new_probs = [0.8, 0.2]  # New probabilities (arbitrary values)
    netica_manager.set_node_probs(node, new_probs)

    # Print the probabilities after changing
    print("\nProbabilities after changing:")
    for i in range(netica_manager.get_node_number_states(node)):
        print(f"State{i + 1}: {netica_manager.get_node_probs(node)[i]}")

    # Cleanup environment
    del netica_manager
