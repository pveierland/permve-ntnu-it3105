from enum import Enum

class State(Enum):
    start                = 1
    expand_node_begin    = 2
    generate_nodes       = 3
    expand_node_complete = 4
    success              = 5
    failed               = 6
