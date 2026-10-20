from models.node import Node

import copy


# ==============================================
# VERIFICAR OBJETIVO
# ==============================================

def is_node_the_goal(node: Node):
    """
    Comprueba si todos los cultivos secos
    del mundo han sido tratados.
    """

    dry_crops = set(node.get_dry_crops())

    treated_crops = set(
        node.get_fertilized_crops()
    )

    return dry_crops.issubset(treated_crops)


# ==============================================
# GENERAR EL SIGUIENTE ESTADO
# ==============================================

def get_next_move_node(
    matrix: list[list[int]],
    next_row: int,
    next_col: int,
    prev_node: Node
):
    """
    Genera un nuevo estado después de mover
    AgroBot a la posición indicada.

    Actualiza:
        - posición
        - fertilizante
        - cultivos tratados
        - estado de la avioneta
        - combustible
        - costo acumulado
        - profundidad
    """

    # ==========================================
    # VALIDAR MOVIMIENTO
    # ==========================================

    rows = len(matrix)
    cols = len(matrix[0])

    current_row, current_col = (
        prev_node.get_bot_pos()
    )

    if not (
        0 <= next_row < rows
        and 0 <= next_col < cols
    ):
        raise ValueError(
            "El movimiento está fuera del tablero."
        )

    distance = (
        abs(next_row - current_row)
        + abs(next_col - current_col)
    )

    if distance != 1:
        raise ValueError(
            "AgroBot solo puede moverse una casilla "
            "en dirección horizontal o vertical."
        )

    if matrix[next_row][next_col] == 1:
        raise ValueError(
            "AgroBot no puede atravesar obstáculos."
        )

    # ==========================================
    # COPIAR INFORMACIÓN DEL ESTADO ANTERIOR
    # ==========================================

    fertilizer_amount = (
        prev_node.get_fertilizer_amount()
    )

    fertilized_crops = list(
        prev_node.get_fertilized_crops()
    )

    plane_boarded = (
        prev_node.get_plane_boarded()
    )

    fuel_remaining = (
        prev_node.get_fuel_remaining()
    )

    fertilized_crop = False

    # ==========================================
    # CALCULAR COSTO DEL MOVIMIENTO
    # ==========================================

    if plane_boarded and fuel_remaining > 0:

        movement_cost = 0.5

        fuel_remaining -= 1

    else:

        movement_cost = 1.0

    # ==========================================
    # IDENTIFICAR LA CASILLA DE DESTINO
    # ==========================================

    next_position = (next_row, next_col)

    # ==========================================
    # RECARGAR FERTILIZANTE
    # ==========================================

    if next_position == prev_node.get_fertilizer_pos():

        fertilizer_amount = 2

    # ==========================================
    # ABORDAR AVIONETA
    # ==========================================

    if next_position == prev_node.get_plane_pos():

        if not plane_boarded:

            plane_boarded = True

    # ==========================================
    # TRATAR CULTIVOS SECOS
    # ==========================================

    if next_position in prev_node.get_dry_crops():

        if (
            fertilizer_amount > 0
            and next_position not in fertilized_crops
        ):

            fertilizer_amount -= 1

            fertilized_crops.append(
                next_position
            )

            fertilized_crop = True

    # ==========================================
    # ACTUALIZAR MATRIZ
    # ==========================================

    new_matrix = copy.deepcopy(matrix)

    previous_position = (
        prev_node.get_bot_pos()
    )

    prev_row, prev_col = previous_position

    # ------------------------------------------
    # RESTAURAR CASILLA ANTERIOR
    # ------------------------------------------

    if previous_position == prev_node.get_fertilizer_pos():

        new_matrix[prev_row][prev_col] = 4

    elif previous_position == prev_node.get_plane_pos():

        new_matrix[prev_row][prev_col] = 5

    elif previous_position in prev_node.get_dry_crops():

        if previous_position in fertilized_crops:

            new_matrix[prev_row][prev_col] = 6

        else:

            new_matrix[prev_row][prev_col] = 3

    else:

        new_matrix[prev_row][prev_col] = 0

    # ------------------------------------------
    # MOVER EL ROBOT
    # ------------------------------------------

    new_matrix[next_row][next_col] = 2

    # ==========================================
    # ACTUALIZAR COSTO ACUMULADO
    # ==========================================

    new_cost = (
        prev_node.get_cost()
        + movement_cost
    )

    # ==========================================
    # ACTUALIZAR PROFUNDIDAD
    # ==========================================

    new_depth = (
        prev_node.get_depth()
        + 1
    )

    # ==========================================
    # CREAR NUEVO NODO
    # ==========================================

    new_node = Node(
        matrix=new_matrix,

        agro_bot_position=next_position,

        fertilizer_position=(
            prev_node.get_fertilizer_pos()
        ),

        plane_position=(
            prev_node.get_plane_pos()
        ),

        dry_crops=(
            prev_node.get_dry_crops()
        ),

        fertilizer_amount=fertilizer_amount,

        fertilized_crop=fertilized_crop,

        fertilized_crops=fertilized_crops,

        parent_node=prev_node,

        plane_boarded=plane_boarded,

        fuel_remaining=fuel_remaining,

        cost=new_cost,

        depth=new_depth
    )

    return new_node