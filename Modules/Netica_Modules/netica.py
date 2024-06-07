# Python 3.9
from ctypes import c_int, c_double
from typing import List, Union, Generator, Optional
from Modules.NeticaPy3.NeticaPy import Netica, NewNode as NeticaNode
from Modules.NeticaPy3.NeticaPy import IntList, FloatList
from weakref import finalize
import os
from enum import Enum
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            logger.warning(f"{password_varname} environment variable for password not set. Netica will not be able to load large networks.")

        # create the netica environment
        self.env = N.NewNeticaEnviron_ns(password.encode('utf-8'), None, b"")
        self.mesg = bytearray(1000)
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
            N.CompileNet_bn(net)
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
            logger.error(f"Error cleaning up Netica environment: {e}")

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
                f"node {self.get_node_name(node)} has no named states. Instead provide the state index (0-{self.get_num_node_states(node) - 1})")
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

    def set_node_probs(self, node: Union[int, str, NeticaNode], parent_states: Optional[List[Union[int, str]]], probs: List[float]):
        """Set the probabilities for a node given its parent states and corresponding probabilities."""
        node = self.get_node(node)

        # Check if the node has parent nodes
        parent_nodes = N.GetNodeParents_bn(node)
        num_parents = N.LengthNodeList_bn(parent_nodes)

        # Print parent nodes if available
        if num_parents > 0:
            logger.info(
                f"Node '{self.get_node_name(node)}', Parent nodes: {parent_nodes}, Number of parents: {num_parents}")
        else:
            logger.info(f"Node '{self.get_node_name(node)}' has no parent nodes")

        # Check if parent_states is None or empty
        if not parent_states:
            if num_parents > 0:
                raise ValueError("Parent states cannot be empty when the node has parent nodes.")

            # Set probabilities without parent states
            logger.info("Setting probabilities without parent states")
            probs_c = FloatList(probs)
            for i in range(1, 100):
                print(i)
            N.SetNodeProbs_bn(node, IntList([]), probs_c)

        else:
            if len(parent_states) != num_parents:
                raise ValueError("Number of parent states provided does not match the number of parents of the node.")

            parent_indices = [self.get_node_state(self.get_node(N.NthNode_bn(parent_nodes, i)), state) for i, state in
                              enumerate(parent_states)]
            logger.info(f"Parent indices: {parent_indices}")

            probs_c = FloatList(probs)
            parent_indices_c = IntList(parent_indices)
            N.SetNodeProbs_bn(node, parent_indices_c, probs_c)

    def cleanup_net(self):
        """Run when the object is garbage collected"""
        N.DeleteNet_bn(self.net)
