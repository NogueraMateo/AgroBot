# ==========================================
# ADMINISTRADOR DE ALGORITMOS DE BÚSQUEDA
# ==========================================

from search.bfs import breadth_search
from search.dfs import depth_search
from search.ucs import uniform_cost_search


# ==========================================
# REGISTRO DE ALGORITMOS
# ==========================================

ALGORITHMS = {

    "No informada": {

        "Amplitud": breadth_search,

        "Costo uniforme": uniform_cost_search,

        "Profundidad evitando ciclos": depth_search,
    },

    "Informada": {

        "Avara": None,

        "A*": None,
    }
}


# ==========================================
# VERIFICAR DISPONIBILIDAD
# ==========================================

def is_algorithm_available(
    search_type,
    algorithm_name
):
    """
    Verifica si el algoritmo seleccionado
    ya tiene una función implementada.
    """

    algorithm = ALGORITHMS.get(
        search_type, {}
    ).get(algorithm_name)

    return callable(algorithm)


# ==========================================
# EJECUTAR ALGORITMO
# ==========================================

def execute_search(
    search_type,
    algorithm_name,
    root_node
):
    """
    Ejecuta el algoritmo correspondiente
    a la selección de la interfaz.
    """

    # Obtener algoritmos disponibles
    search_group = ALGORITHMS.get(
        search_type
    )

    if search_group is None:

        raise ValueError(
            f"Tipo de búsqueda no válido: {search_type}"
        )

    # Obtener algoritmo seleccionado
    if algorithm_name not in search_group:

        raise ValueError(
            f"Algoritmo no válido: {algorithm_name}"
        )

    algorithm = search_group[algorithm_name]

    # Verificar si está implementado
    if algorithm is None:

        raise NotImplementedError(
            f"El algoritmo '{algorithm_name}' "
            f"todavía no está implementado."
        )

    # Ejecutar búsqueda
    result = algorithm(root_node)

    return result