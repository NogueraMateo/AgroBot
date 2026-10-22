from queue import Queue

from models.node import Node
from search.helpers import generate_successors, is_node_the_goal, reconstruct_path

import time

    

def breadth_search(root: Node):

    queue = Queue()

    start_time = time.perf_counter()

    queue.put(root)

    expanded_nodes = 0

    visited_states = {root.get_state_key()}

    while not queue.empty():
        node:Node = queue.get()

        if is_node_the_goal(node):
            solution_path = reconstruct_path(node)
            return {
                "found": True,
                "path": solution_path,
                "cost": node.get_cost(),
                "expanded_nodes": expanded_nodes,
                "depth": node.get_depth(),
                "execution_time": time.perf_counter() - start_time,
                "status": "Solución encontrada"
            }

        successors = generate_successors(node, visited_states)   
        for successor in successors:
            queue.put(successor)


        expanded_nodes += 1


    return {
        "found": False,
        "path": [],
        "cost": 0,
        "expanded_nodes": expanded_nodes,
        "depth": 0,
        "execution_time": time.perf_counter() - start_time,
        "status": "No se encontró solución"
    }