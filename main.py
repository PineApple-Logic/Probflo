from Modules.NeticaPy3.NeticaPy import Netica

# Path to the .neta file
NETWORK_FILE = 'Modules/Netica_Modules/Balule.neta'


def print_end_node_beliefs(net):
    # Get the beliefs of the end nodes
    end_node_names = []
    i = 0
    while True:
        try:
            # Get the name of the node at index i
            node_name = N.GetNodeName_bn(i).decode()
            if node_name.endswith('_END'):
                end_node_names.append(node_name)
            i += 1
        except:
            # Break the loop when an exception occurs, indicating we have reached the end of the nodes
            break

    # Print the beliefs of the end nodes
    for node_name in end_node_names:
        # Get the node object by name
        node = net.GetNode(node_name.encode(), False)  # Pass net object here

        # Get the belief for the first state
        belief = N.GetNodeBelief_bn(node, 0)
        print(f"Belief for {node_name}: {belief}")


def print_all_node_names(net):
    node_names = []
    i = 0
    while True:
        try:
            # Get the name of the node at index i
            node_name = N.GetNodeName_bn(i).decode()
            node_names.append(node_name)
            i += 1
        except:
            # Break the loop when an exception occurs, indicating we have reached the end of the nodes
            break

    # Print all node names
    for node_name in node_names:
        print(node_name)


if __name__ == '__main__':
    # Initialize Netica environment
    N = Netica()
    env = N.NewNeticaEnviron_ns(b"", None, b"")
    mesg = bytearray()
    res = N.InitNetica2_bn(env, mesg)

    # Check if initialization was successful
    if res != 0:
        print(f"Initialization failed: {mesg.decode()}")
        exit(1)

    # Create a NeticaPy.Stream object
    file_stream = N.NewFileStream_ns(NETWORK_FILE.encode(), None)

    # Directly load Bayesian network structure from .neta file
    net = N.ReadNet_bn(file_stream, True)

    # Check if network file was loaded correctly
    if net is None:
        print("Failed to load network file.")
        exit(1)
    else:
        print("Network file loaded successfully.")

    # Print names of all nodes
    print("All node names:")
    print_all_node_names(net)

    # Print beliefs of end nodes
    print("\nBeliefs of end nodes:")
    print_end_node_beliefs(net)

    # Cleanup
    N.DeleteNet_bn(net)
    N.CloseNetica_bn(env, mesg)