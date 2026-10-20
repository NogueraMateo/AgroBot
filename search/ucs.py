import heapq
import time

from itertools import count

from models.node import get_next_possible_operators
from models.operators import AgroBotOperators

from search.helpers import (
    get_next_move_node,
    is_node_the_goal
)


# ==========================================
# DIRECCIONES DE MOVIMIENTO
# ==========================================

# Conservamos la convención que actualmente
# utiliza el código de AgroBot.

MOVEMENTS = {
    AgroBotOperators.UP: (1, 0),
    AgroBotOperators.DOWN: (-1, 0),
    AgroBotOperators.RIGHT: (0, 1),
    AgroBotOperators.LEFT: (0, -1),
}


# ==========================================
# RECONSTRUIR LA SOLUCIÓN
# ==========================================

def reconstruct_path(goal_node):
    """
    Reconstruye la secuencia de nodos
    desde el estado inicial hasta el objetivo.
    """

    path = []

    current_node = goal_node

    while current_node is not None:

        path.append(current_node)

        current_node = current_node.parent_node

    # Los nodos se recorrieron desde el
    # objetivo hasta el estado inicial.
    path.reverse()

    return path


# ==========================================
# GENERAR SUCESORES
# ==========================================

def generate_successors(node):
    """
    Genera los estados a los que AgroBot
    puede llegar mediante un movimiento.
    """

    successors = []

    current_row, current_col = node.get_bot_pos()

    # Obtener movimientos válidos
    possible_operators = get_next_possible_operators(
        node
    )

    for operator in possible_operators:

        # Obtener desplazamiento
        delta_row, delta_col = MOVEMENTS[operator]

        # Calcular nueva posición
        next_row = current_row + delta_row
        next_col = current_col + delta_col

        # Crear el siguiente estado
        next_node = get_next_move_node(
            node.get_matrix(),
            next_row,
            next_col,
            node
        )

        successors.append(next_node)

    return successors


# ==========================================
# BÚSQUEDA POR COSTO UNIFORME
# ==========================================

def uniform_cost_search(root_node, max_expanded=200000):
    """
    Implementa búsqueda por costo uniforme.

    Parámetros:
        root_node:
            Estado inicial del problema.

        max_expanded:
            Límite de seguridad de nodos
            expandidos.

    Devuelve un diccionario con:
        - found
        - path
        - cost
        - expanded_nodes
        - depth
        - execution_time
        - status
    """

    # ======================================
    # INICIAR MEDICIÓN DE TIEMPO
    # ======================================

    start_time = time.perf_counter()

    # ======================================
    # COLA DE PRIORIDAD
    # ======================================

    priority_queue = []

    # Identificador para resolver empates
    tie_breaker = count()

    # Insertar estado inicial
    heapq.heappush(
        priority_queue,
        (
            root_node.get_cost(),
            next(tie_breaker),
            root_node
        )
    )

    # ======================================
    # MEJOR COSTO CONOCIDO POR ESTADO
    # ======================================

    best_cost = {
        root_node.get_state_key(): root_node.get_cost()
    }

    # Estados que ya fueron expandidos
    expanded_states = set()

    expanded_nodes = 0

    # ======================================
    # CICLO PRINCIPAL
    # ======================================

    while priority_queue:

        # ----------------------------------
        # EXTRAER EL NODO MÁS ECONÓMICO
        # ----------------------------------

        current_cost, _, current_node = heapq.heappop(
            priority_queue
        )

        state_key = current_node.get_state_key()

        # ----------------------------------
        # DESCARTAR RUTAS MÁS COSTOSAS
        # ----------------------------------

        if current_cost > best_cost.get(
            state_key,
            float("inf")
        ):
            continue

        # Evitar expandir el mismo estado
        # más de una vez.
        if state_key in expanded_states:
            continue

        # ----------------------------------
        # COMPROBAR OBJETIVO
        # ----------------------------------

        if is_node_the_goal(current_node):

            execution_time = (
                time.perf_counter() - start_time
            )

            solution_path = reconstruct_path(
                current_node
            )

            return {
                "found": True,
                "path": solution_path,
                "cost": current_node.get_cost(),
                "expanded_nodes": expanded_nodes,
                "depth": current_node.get_depth(),
                "execution_time": execution_time,
                "status": "Solución encontrada"
            }

        # ----------------------------------
        # LÍMITE DE SEGURIDAD
        # ----------------------------------

        if expanded_nodes >= max_expanded:

            return {
                "found": False,
                "path": [],
                "cost": None,
                "expanded_nodes": expanded_nodes,
                "depth": None,
                "execution_time": (
                    time.perf_counter() - start_time
                ),
                "status": "Límite de expansión alcanzado"
            }

        # ----------------------------------
        # MARCAR ESTADO COMO EXPANDIDO
        # ----------------------------------

        expanded_states.add(state_key)

        expanded_nodes += 1

        # ----------------------------------
        # GENERAR SUCESORES
        # ----------------------------------

        successors = generate_successors(
            current_node
        )

        for successor in successors:

            successor_key = successor.get_state_key()

            successor_cost = successor.get_cost()

            # --------------------------------
            # COMPARAR COSTOS
            # --------------------------------

            previous_cost = best_cost.get(
                successor_key,
                float("inf")
            )

            # Solo conservar una ruta si
            # mejora el costo conocido.
            if successor_cost < previous_cost:

                best_cost[successor_key] = successor_cost

                heapq.heappush(
                    priority_queue,
                    (
                        successor_cost,
                        next(tie_breaker),
                        successor
                    )
                )

    # ======================================
    # NO SE ENCONTRÓ SOLUCIÓN
    # ======================================

    execution_time = (
        time.perf_counter() - start_time
    )

    return {
        "found": False,
        "path": [],
        "cost": None,
        "expanded_nodes": expanded_nodes,
        "depth": None,
        "execution_time": execution_time,
        "status": "No se encontró una solución"
    }