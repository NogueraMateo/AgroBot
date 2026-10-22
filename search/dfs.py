

from models.node import Node
from search.helpers import generate_successors, is_node_the_goal, reconstruct_path


def depth_search(root: Node):

    stack = [root]

    expanded_nodes = 0

    visited_states = {root.get_state_key()}

    while len(stack) > 0:
        current_node = stack.pop()


        if is_node_the_goal(current_node):
            solution_path = reconstruct_path(current_node)
            return {
                "found": True,
                "path": solution_path,
                "cost": current_node.get_cost(),
                "expanded_nodes": expanded_nodes,
                "depth": current_node.get_depth(),
                "execution_time": 0,
                "status": "Solución encontrada"
            }


        successors = generate_successors(current_node, visited_states)
        successors.reverse()
        stack.extend(successors)


        expanded_nodes += 1

    return {
        "found": False,
        "path": [],
        "cost": 0,
        "expanded_nodes": expanded_nodes,
        "depth": 0,
        "execution_time": 0,
        "status": "No se encontró solución"
    }