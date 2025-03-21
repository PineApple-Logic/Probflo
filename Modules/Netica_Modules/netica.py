# Python 3.9
import sys
import random
import ctypes as ct
from ctypes import POINTER, c_double, cast
from typing import List, Union, Generator, Optional
from Modules.NeticaPy3.NeticaPy import Netica, NewNode as NeticaNode
from weakref import finalize
import os
from enum import Enum
from loguru import logger

# Setup logger
logger.remove()
level = 'INFO'  # Set the level of logging (DEBUG/INFO/WARNINGS/ERRORS/CRITICAL)
logger.add(sys.stdout, format="<green>[{module}]</green><red>:</red><green>[{line}]</green>"
                              "  <level>{level}<red>:</red> {message}</level>", level=level)


class Checking(Enum):
    NO_CHECK = 1
    QUICK_CHECK = 2
    REGULAR_CHECK = 3
    COMPLETE_CHECK = 4
    QUERY_CHECK = -1


class ErrorSeverity(Enum):
    NOTHING_ERR = 1
    REPORT_ERR = 2
    NOTICE_ERR = 3
    WARNING_ERR = 4
    ERROR_ERR = 5
    XXX_ERR = 6


class ErrorCondition(Enum):
    OUT_OF_MEMORY_CND = 0x08
    USER_ABORTED_CND = 0x20
    FROM_WRAPPER_CND = 0x40
    FROM_DEVELOPER_CND = 0x80
    INCONS_FINDING_CND = 0x200


class EventType(Enum):
    CREATE_EVENT = 0x01
    DUPLICATE_EVENT = 0x02
    REMOVE_EVENT = 0x04


class NodeType(Enum):
    CONTINUOUS_TYPE = 1
    DISCRETE_TYPE = 2
    TEXT_TYPE = 3


class NodeKind(Enum):
    NATURE_NODE = 1
    CONSTANT_NODE = 2
    DECISION_NODE = 3
    UTILITY_NODE = 4
    DISCONNECTED_NODE = 5
    ADVERSARY_NODE = 6


class State(Enum):
    EVERY_STATE = -5
    IMPOSS_STATE = -4
    UNDEF_STATE = -3


class CasePosition(Enum):
    FIRST_CASE = -15
    NEXT_CASE = -14
    NO_MORE_CASES = -13


class Sensitivity(Enum):
    ENTROPY_SENSV = 0x02
    REAL_SENSV = 0x04
    VARIANCE_SENSV = 0x100
    VARIANCE_OF_REAL_SENSV = 0x104


N = Netica()


class NeticaManager:
    def __init__(self, password_varname="NETICA_PASSWORD"):
        # get the password from the environment variable
        password = os.environ.get(password_varname, default="")
        if not password:
            logger.warning(
                f"{password_varname} environment variable for password not set."
                f" Netica will not be able to load large networks.")

        # create the netica environment
        INFINITY_ns = N.GetInfinityDbl_ns()

        self.env = N.NewNeticaEnviron_ns(password.encode('utf-8'), None, b"")

        self.mesg = bytearray()

        self.res = N.InitNetica2_bn(self.env, self.mesg)
        logger.info("Netica initialization message:\n" + self.mesg.decode("utf-8"))

        self.finalizer = finalize(self, self.cleanup_env)

    def new_graph(self, path: str) -> "NeticaGraph":
        # ensure that the file exists
        try:
            with open(path, 'r'):
                pass
        except FileNotFoundError:
            logger.error(f"File not found: {path}")
            raise
        except IOError as e:
            logger.error(f"Error opening file {path}: {e}")
            raise

        # load the network
        try:
            path = path.encode('utf-8')
            net = N.ReadNet_bn(N.NewFileStream_ns(path, self.env, b""), 0)
            logger.debug(net)
            N.CompileNet_bn(net)
            logger.debug(N.LengthNodeList_bn(N.GetNetNodes_bn(net)))

            logger.debug("Compiled Network")
            return NeticaGraph(net, self)
        except Exception as e:
            logger.error(f"Error loading or compiling network from {path}: {e}")
            raise

    def cleanup_env(self):
        """cleanup the netica environment when the manager is destroyed"""
        try:
            res = N.CloseNetica_bn(self.env, self.mesg)
            logger.info(self.mesg.decode("utf-8"))
        except Exception as e:
            logger.error(f'Error cleaning up Netica environment: {e}')


class NeticaGraph:
    def __init__(self, net, manager: NeticaManager):
        self.net = net
        self.manager = manager

        self.node_names = {self.get_node_name(i): i for i in range(self.get_num_nodes())}
        self.node_state_names = {
            self.get_node_name(i): {self.get_node_state_name(i, j): j for j in range(self.get_num_node_states(i))} for i
            in range(self.get_num_nodes())}

        # replace node state names that only had empty strings, with None
        for node_name, state_names in self.node_state_names.items():
            if len(state_names) == 1 and list(state_names.keys())[0] == "":
                self.node_state_names[node_name] = None
            # else:
            # self.node_state_names[node_name] = state_names

        self.finalizer = finalize(self, self.cleanup_net)

    def get_num_nodes(self) -> int:
        """get the number of nodes in a network"""
        return N.LengthNodeList_bn(N.GetNetNodes_bn(self.net))

    def net_itr(self) -> Generator[NeticaNode, None, None]:
        """iterator over the nodes in a network"""
        nodes = N.GetNetNodes_bn(self.net)

        for i in range(N.LengthNodeList_bn(nodes)):
            yield N.NthNode_bn(N.GetNetNodes_bn(self.net), i)

    def get_node_by_index(self, node_idx: int) -> NeticaNode:
        """get a node by its index"""
        return N.NthNode_bn(N.GetNetNodes_bn(self.net), node_idx)

    def get_node_by_name(self, node_name: str) -> NeticaNode:
        """get a node by its name. (make sure that the self.node_names dict is populated before calling this)"""
        try:
            node_idx = self.node_names[node_name]
        except KeyError:
            raise KeyError(f"node `{node_name}` does not exist in this network") from None
        return self.get_node_by_index(node_idx)

    def get_node(self, node: Union[int, str, NeticaNode]) -> NeticaNode:
        """get a node by either its index or name"""
        if isinstance(node, str):
            return self.get_node_by_name(node)
        elif isinstance(node, int):
            return self.get_node_by_index(node)
        elif isinstance(node, NeticaNode):
            return node
        else:
            raise TypeError(f"node must be either a string, int, or NeticaNode, not {type(node)}")

    def get_node_name(self, node: Union[int, str, NeticaNode]) -> str:
        """get the name of a node"""
        node = self.get_node(node)
        return N.GetNodeName_bn(node).decode('utf-8')

    def get_node_type(self, node: Union[int, str, NeticaNode]) -> NodeType:
        """get the type of a node. node may be either the index, or the name of the node"""
        node = self.get_node(node)
        raw_type = N.GetNodeType_bn(node)
        return NodeType(raw_type)

    def get_node_kind(self, node: Union[int, str, NeticaNode]) -> NodeKind:
        """get the kind of a node"""
        node = self.get_node(node)
        raw_kind = N.GetNodeKind_bn(node)
        return NodeKind(raw_kind)

    def get_num_node_states(self, node: Union[int, str, NeticaNode]) -> int:
        """get the number of states a node can take on, or 0 if it is a continuous node"""
        node = self.get_node(node)
        return N.GetNodeNumberStates_bn(node)

    def check_node_state_index_valid(self, node: Union[int, str, NeticaNode], state_idx: int):
        """checks that the state index is valid"""
        node = self.get_node(node)
        num_states = self.get_num_node_states(node)
        if state_idx >= num_states:
            raise ValueError(f"state_idx given ({state_idx}) must be less than the number of states ({num_states})")
        if state_idx < 0:
            raise ValueError(f"state_idx given ({state_idx}) must be greater than or equal to 0")

    def get_node_state_by_name(self, node: Union[int, str, NeticaNode], state_name: str) -> int:
        """get the index of a state of a node, given its name. Mainly just checks that the state name is valid"""
        node = self.get_node(node)
        state_map = self.node_state_names[self.get_node_name(node)]
        if state_map is None:
            raise ValueError(
                f"node {self.get_node_name(node)} has no named states. Instead provide the state index "
                f"(0-{self.get_num_node_states(node) - 1})")
        if state_name not in state_map:
            raise ValueError(f"invalid state_name '{state_name}'. Must be one of {list(state_map.keys())}")
        return state_map[state_name]

    def get_node_state(self, node: Union[int, str, NeticaNode], state: Union[int, str]) -> int:
        """get the index of a state of a node, given its name or index"""
        node = self.get_node(node)
        if isinstance(state, int):
            self.check_node_state_index_valid(node, state)
            return state
        elif isinstance(state, str):
            return self.get_node_state_by_name(node, state)
        else:
            raise TypeError(f"state must be either a string or int, not {type(state)}")

    def get_node_state_name(self, node: Union[int, str, NeticaNode], state: Union[int, str]) -> str:
        # TODO: -> node comes from net_itr... maybe make this just take in the index of the node?
        """get the name of a state of a node"""
        node = self.get_node(node)
        state_index = self.get_node_state(node, state)
        return N.GetNodeStateName_bn(node, state_index).decode('utf-8')

    def enter_finding(self, node: Union[int, str, NeticaNode], state: Union[int, str], *, retract=False, verbose=False):
        node = self.get_node(node)
        node_name = self.get_node_name(node)

        # retract finding. Certain nodes require this before entering a new finding
        if retract:
            N.RetractNodeFindings_bn(node)
            if verbose:
                logger.info(f"retracting {node_name}")

        # enter finding via the state index
        state_index = self.get_node_state(node, state)
        N.EnterFinding_bn(node, state_index)
        if verbose:
            logger.info(f"setting {node_name} to {state}")

    def get_node_belief(self, node: Union[int, str, NeticaNode], state: Union[int, str]) -> float:
        node = self.get_node(node)
        node_name = self.get_node_name(node)
        node_state = self.get_node_state_name(node, state)
        belief = N.GetNodeBelief(node_name.encode('utf-8'), node_state.encode('utf-8'), self.net)
        return belief

    def get_node_finding(self, node: Union[int, str, NeticaNode]) -> int:
        """Get the finding of a node."""
        node = self.get_node(node)
        finding = N.GetNodeFinding_bn(node)
        return finding
        # Generate three random float numbers between 0 and 1

    def set_node_probs_randomly(self, node: Union[int, str, NeticaNode], parent_states: Optional[List[Union[int, str]]],
                                probs: List[float]):
        """Set the probabilities of a node randomly."""
        states_array = list(range(len(parent_states)))
        r1, r2, r3 = sorted([random.random() for _ in range(3)])
        f1 = r1
        f2 = r2 - r1
        f3 = r3 - r2
        f4 = 1 - r3
        random_floats = [f1, f2, f3, f4]

        if parent_states != None and len(
                states_array) < 5:  # Check if the number of parent states is less than 5 i.e. ignore the last couple in json and set the probabilities
            N.SetNodeProbs(node, *random_floats)
            logger.error(N.ErrorMessage_ns(N.GetError_ns(N, 5, 0)).decode("utf-8"))

    def NodeStates(self, node, naming='statename'):
        # returns the states of a node based on the naming convention
        cnode = N.GetNodeNamed_bn(node, self.net)  # Get the node object
        y = N.GetNodeNumberStates_bn(cnode)  # Get the number of states
        states = []
        for j in range(y):
            if naming == 'statename':
                states.append(ct.cast(N.GetNodeStateName_bn(cnode, j), ct.c_char_p).value)  # Get the state name
            elif naming == 'titlename':
                states.append(ct.cast(N.GetNodeStateTitle_bn(cnode, j), ct.c_char_p).value)  # Get the state title
        return states

    def ParentNodeStates(self, node, naming='statename'):
        # returns the states of a parent node based on the naming convention
        cnode = N.GetNodeNamed_bn(node, self.net)
        y = N.GetNodeNumberStates_bn(cnode)
        states = []
        for j in range(y):
            if naming == 'statename':
                states.append(N.GetNodeStateName_bn(cnode, j))
                # print(j," :",N.GetNodeStateName_bn(cnode, j))
            elif naming == 'titlename':
                states.append(ct.cast(N.GetNodeStateTitle_bn(cnode, j), ct.c_char_p).value)
        return states

    def get_node_probabilities(self, node_name, parent_node_name, parent_state_names):
        """
        Fetches the probabilities of a node given the names of parent states.
        """

        # Fetch node states
        parent_node_states = self.NodeStates(parent_node_name)

        # Convert state names to indices
        parent_state_indices = []
        for state_name in parent_state_names:
            try:
                state_index = parent_node_states.index(state_name)
                parent_state_indices.append(state_index)
            except ValueError:
                raise ValueError(f"State name {state_name} not found in parent node states.")

        # Call the API function
        # print(parent_state_indices)
        probabilities = N.GetNodeProbs_bn(node_name, parent_state_indices)

        return probabilities

    def normalize_probabilities(self, probs):
        total = sum(probs)
        if total == 0:
            raise ValueError("Sum of probabilities is zero, cannot normalize")
        # Scale each probability proportionally to make the sum approximately 1
        normalized_probs = [round(p / total, 3) for p in probs]
        # Ensure the normalization is exact by adjusting the last element
        diff = round(1 - sum(normalized_probs), 3)
        normalized_probs[-1] += diff
        # Format each probability to one decimal place
        formatted_probs = [float(f"{p:.6f}") for p in normalized_probs]

        return formatted_probs

    def set_node_probabilities(self, node_name, parent_node_name, parent_state_names, probabilities):
        """
        Sets the probabilities of a node given the names of parent states.
        """
        error = ""
        N.RetractNodeFindings_bn(node_name)

        logger.info("----------------- Info about the node -----------------")
        logger.info(f'Node name: {parent_node_name}')
        logger.info(f'Node kind: {N.GetNodeKind_bn(node_name)}')
        node_kind = N.GetNodeKind_bn(node_name)
        node_desc = [
            {
                "type": "NATURE_NODE",
                "description": "Bayes nets are composed only of this type (and constant nodes).",
                "details": "This is a 'chance' or 'deterministic' node of an influence diagram."
            },
            {
                "type": "DECISION_NODE",
                "description": "Indicates a variable that can be controlled.",
                "details": "This is a 'decision' node of an influence diagram."
            },
            {
                "type": "UTILITY_NODE",
                "description": "A variable to maximize the expected value of.",
                "details": "This is a 'value' node of an influence diagram."
            },
            {
                "type": "CONSTANT_NODE",
                "description": "A fixed parameter, useful as an equation constant.",
                "details": "When its value changes, equations should be reconverted to CPT tables, and maybe the net recompiled."
            },
            {
                "type": "DISCONNECTED_NODE",
                "description": "The (virtual) parent node of a link which has been disconnected.",
                "details": "See example code below."
            }
        ]

        logger.debug(node_desc[node_kind-1])
        node_children_names = [N.GetNodeName_bn(N.NthNode_bn(N.GetNodeChildren_bn(node_name), i)) for i in range(N.LengthNodeList_bn(N.GetNodeChildren_bn(node_name)))]
        logger.debug(f'Node children: {node_children_names}')

        parent_node_states = self.NodeStates(parent_node_name)
        stored_likelihood = N.GetNodeLikelihood_bn(node_name)

        logger.debug("----------------- Likelihoods -----------------")
        state_likelihood_array = [f"{state}: {likelihood}" for state, likelihood in zip(parent_node_states, stored_likelihood)]
        logger.debug(f'State:Likelihood {state_likelihood_array}')

        error = N.ErrorMessage_ns(N.GetError_ns(N, 5, 0)).decode("utf-8")
        if error:
            print("--------- Error retrieving likelihoods ----------")
            logger.error(f"{error} for {parent_node_name}")
            print()
            error = ""

        parent_state_indices = [parent_node_states.index(state_name) for state_name in parent_state_names]
        parent_probs = [N.GetNodeBelief(parent_node_name, state, self.net) for state in parent_node_states]
        if parent_probs is None:
            raise ValueError("Parent probabilities are None")

        contains_zero = False
        probabilities_list = []
        unedited_probabilities = []
        key_names = []
        parent_int = [int(i) for i in parent_state_indices]
        count = 0
        original_values = []
        for key, value in probabilities.items():
            key_names.append(key)
            try:
                float_value = float(f"{round(value, 3):.6f}")
                if isinstance(float_value, float):
                    if float_value < 0.00000001 or float_value <= 0.0:
                        probabilities_list.append(0.001)
                        unedited_probabilities.append(0.0)
                        contains_zero = True
                        count += 1
                    else:
                        unedited_probabilities.append(float_value)
                        probabilities_list.append(float_value)
            except ValueError:
                logger.warning(f"Warning: Value for '{key}' cannot be converted to float and will be skipped.")

        sum_probabilities = sum(probabilities_list)
        if sum_probabilities != 1:
            original_probabilities = probabilities_list.copy()
            probabilities_list = self.normalize_probabilities(probabilities_list).copy()
            logger.info(f"Sum of probabilities: {sum(probabilities_list)}")
            print()
            print("----------------- Normalization -----------------")
            if contains_zero:
                logger.warning(f"Probabilities have been normalized and 0 values replaced with 0.001 "
                               f"for node with parent node: {parent_node_name}")
            else:
                logger.info(f"Probabilities have been normalized for node with parent node: {parent_node_name}")
            logger.info(f"Original probabilities: {original_probabilities}")
            logger.info(f"Updated probabilities: {probabilities_list}")
            print()

        if parent_state_names is not None and len(parent_state_names) == len(probabilities_list):
            if N.GetNodeType_bn(node_name) == 2:  # node type is discrete
                logger.debug(f'Node findings are the following: {N.GetNodeFinding_bn(node_name)}')
                number_state_names = [float(f"{round(float(key), 3):.6f}") for key in key_names if isinstance(float(f"{round(float(key), 3):.6f}"), float)]
                parent_state_names_length = len(parent_state_names)
                node_levels = N.GetNodeLevels_bn(node_name)
                level_data = [node_levels[level] for level in range(parent_state_names_length)]
                if level_data != node_levels:
                    print()
                    logger.warning("----------------- Node levels Not The Same -----------------")
                    print()
                    logger.info("----------------- Original Node levels -----------------")
                    logger.info(level_data)
                    N.SetNodeLevels_bn(node_name, parent_state_names_length, number_state_names)
                    level_data = [node_levels[level] for level in range(parent_state_names_length)]
                    print()
                    logger.info("----------------- Updating Node levels to -----------------")
                    logger.info(level_data)
                    print()
                logger.info("----------------- Using unedited Probabilities -----------------")
                logger.info(f'Probabilities list: {unedited_probabilities}')
                logger.info(f'Size of unedited_probabilities list: {len(unedited_probabilities)}')
                logger.info(f'Size of node levels: {len(level_data)}')
                print()
                level_data_length = len(level_data)
                array_of_integers = list(range(level_data_length))
                try:
                    N.EnterNodeLikelihood_bn(node_name, unedited_probabilities)
                    error = N.ErrorMessage_ns(N.GetError_ns(N, 5, 0)).decode('utf-8')
                    if error:
                        logger.error('--------- Error with setting likelihood probabilities ----------')
                        logger.error(f'{error} for {parent_node_name}')
                        print()
                        error = ''
                except Exception as e:
                    logger.error('--------- Error with setting probabilities ----------')
                    logger.error(f'An error occurred while setting probabilities: {str(e)}')
                    print()
                    error = ''
            else:
                print()
                N.SetNodeProbs(node_name, *probabilities_list)
                logger.info('<----------------- Updating probabilities ----------------->')
                error = N.ErrorMessage_ns(N.GetError_ns(N, 5, 0)).decode('utf-8')
                if error != '':
                    logger.error('-------------- Netica Else Error --------------')
                    logger.error(f'{error} for {parent_node_name}')
                    print()
                    error = ''
        else:
            node_levels = N.GetNodeLevels_bn(node_name)
            print(f'Node levels: {node_levels}')
            parent_state_names = self.ParentNodeStates(parent_node_name)
            print(f'Is node deterministic: {N.GetNodeType_bn(node_name)}')
            logger.error('-------------- Node probabilities not updated --------------')
            logger.warning(f'Node with issues: {parent_node_name}')
            logger.warning(f'State probabilities submitted {len(probabilities_list)}'
                           f" don't align with number of possible states specified in json.")
            logger.warning(f'The parent states are: {parent_state_names}')
            logger.warning(parent_int)
            logger.warning(probabilities_list)
            logger.warning(f'The states in json are f{key_names}')
            print()

    def NodeProbs(self, node, naming='statename'):
        """
        returns the states of a node
        """
        cnode = N.GetNodeNamed_bn(node, self.net)
        y = N.GetNodeNumberStates_bn(cnode)
        states = []
        for j in range(y):
            if naming == 'statename':
                states.append(ct.cast(N.GetNodeProbs_bn(cnode, j), ct.c_char_p).value)
            elif naming == 'titlename':
                states.append(ct.cast(N.GetNodeProbs_bn(cnode, j), ct.c_char_p).value)
        return states

    def get_float_list_values(self, float_list_object, expected_length):
        """
        Accesses the internal float values of a FloatList object using ctypes.

        Args:
            float_list_object: The FloatList object.
            expected_length: The expected number of elements in the FloatList.

        Returns:
            A list of float values.
        """
        # Assuming the object has a pointer to an array of doubles
        float_list_pointer = ct.cast(float_list_object, POINTER(c_double * expected_length))
        logger.debug(float_list_pointer)
        # Retrieve values from the array
        float_array = [float_list_pointer.contents[i] for i in range(expected_length)]

        return float_array

    def cleanup_net(self):
        """Run when the object is garbage collected"""
        N.DeleteNet_bn(self.net)
