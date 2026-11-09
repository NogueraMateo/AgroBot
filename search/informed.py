import heapq
import time

from itertools import count
from search.helpers import generate_successors, is_node_the_goal, reconstruct_path


# ==========================================
# HEURÍSTICA DE CULTIVOS PENDIENTES
# ==========================================

def estimate_remaining_cost(node):
    pending_crops = set(node.get_dry_crops()).difference(
        node.get_fertilized_crops()
    )

    row, col = node.get_bot_pos()

    farthest_distance = max(
        (
            abs(row - crop_row) + abs(col - crop_col)
            for crop_row, crop_col in pending_crops
        ),
        default=0
    )

    # Cada movimiento cuesta al menos 0.5 y
    # puede tratar como máximo un cultivo.
    return 0.5 * max(farthest_distance, len(pending_crops))


# ==========================================
# BÚSQUEDA AVARA Y A*
# ==========================================

def greedy_search(root_node, max_expanded=200000):
    """Prioriza los nodos por su costo restante estimado."""
    return _informed_search(root_node, max_expanded, estimate_remaining_cost)


def a_star_search(root_node, max_expanded=200000):
    """Prioriza los nodos por la suma de g(n) y h(n)."""
    def priority(node):
        return node.get_cost() + estimate_remaining_cost(node)

    return _informed_search(root_node, max_expanded, priority)


def _informed_search(root_node, max_expanded, priority):
    start_time = time.perf_counter()
    tie_breaker = count()

    priority_queue = [
        (priority(root_node), next(tie_breaker), root_node)
    ]
    best_cost = {
        root_node.get_state_key(): root_node.get_cost()
    }

    expanded_nodes = 0
    goal_node = None
    status = "No se encontró una solución"

    while priority_queue:

        _, _, current_node = heapq.heappop(priority_queue)
        state_key = current_node.get_state_key()

        # Descartar rutas reemplazadas por una de menor costo.
        if current_node.get_cost() > best_cost[state_key]:
            continue

        if is_node_the_goal(current_node):

            goal_node = current_node
            status = "Solución encontrada"
            break

        if expanded_nodes >= max_expanded:

            status = "Límite de expansión alcanzado"
            break

        expanded_nodes += 1

        for successor in generate_successors(current_node):

            successor_key = successor.get_state_key()
            successor_cost = successor.get_cost()

            # Una mejora de costo puede reabrir un estado.
            if successor_cost < best_cost.get(successor_key, float("inf")):

                best_cost[successor_key] = successor_cost

                heapq.heappush(
                    priority_queue,
                    (priority(successor), next(tie_breaker), successor)
                )

    execution_time = time.perf_counter() - start_time
    found = goal_node is not None

    return {
        "found": found,
        "path": reconstruct_path(goal_node) if found else [],
        "cost": goal_node.get_cost() if found else None,
        "expanded_nodes": expanded_nodes,
        "depth": goal_node.get_depth() if found else None,
        "execution_time": execution_time,
        "status": status
    }
