def read_nodes_from_file(file_path='dump.txt'):
    nodes_data = {}

    with open(file_path, 'r') as file:
        current_node = None
        for line in file:
            line = line.strip()
            if not line:
                continue  # Skip empty lines

            if line.endswith('_END'):
                current_node = line
                nodes_data[current_node] = {}
            else:
                parts = line.split('|')
                if len(parts) == 2:
                    attribute, value = parts[0].strip(), float(parts[1].strip())
                    nodes_data[current_node][attribute] = value

    return nodes_data

