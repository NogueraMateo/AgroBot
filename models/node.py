from .operators import AgroBotOperators


class Node:

    def __init__(
        self,
        matrix: list[list[int]],
        agro_bot_position: tuple[int, int],
        fertilizer_position: tuple[int, int],
        plane_position: tuple[int, int],
        dry_crops: list[tuple[int, int]],
        fertilizer_amount: int = 0,
        fertilized_crop: bool = False,
        fertilized_crops: list[tuple[int, int]] = None,
        parent_node: "Node" = None,
        plane_boarded: bool = False,
        fuel_remaining: int = 30,
        cost: float = 0.0,
        depth: int = 0
    ):

        # ======================================
        # INFORMACIÓN DEL MUNDO
        # ======================================

        self.matrix = matrix

        self.fertilizer_position = fertilizer_position
        self.plane_position = plane_position

        self.dry_crops = dry_crops

        # ======================================
        # ESTADO DEL ROBOT
        # ======================================

        self.agro_bot_position = agro_bot_position

        self.fertilizer_amount = fertilizer_amount

        self.fertilized_crop = fertilized_crop

        self.fertilized_crops = (
            list(fertilized_crops)
            if fertilized_crops is not None
            else []
        )

        # ======================================
        # ESTADO DE LA AVIONETA
        # ======================================

        self.plane_boarded = plane_boarded

        self.fuel_remaining = fuel_remaining

        # ======================================
        # INFORMACIÓN DE BÚSQUEDA
        # ======================================

        self.parent_node = parent_node

        self.cost = cost

        self.depth = depth

    # ==========================================
    # REPRESENTACIÓN DEL NODO
    # ==========================================

    def __str__(self):

        return (
            f"\nNode"
            f"\nPosición: {self.agro_bot_position}"
            f"\nFertilizante: {self.fertilizer_amount}/2"
            f"\nCultivos tratados: {self.fertilized_crops}"
            f"\nAvioneta abordada: {self.plane_boarded}"
            f"\nCombustible: {self.fuel_remaining}/30"
            f"\nCosto acumulado: {self.cost}"
            f"\nProfundidad: {self.depth}"
        )

    # ==========================================
    # MÉTODOS EXISTENTES
    # ==========================================

    def get_matrix(self):
        return self.matrix

    def get_bot_pos(self):
        return self.agro_bot_position

    def get_fertilizer_amount(self):
        return self.fertilizer_amount

    def get_fertilizer_pos(self):
        return self.fertilizer_position

    def get_plane_pos(self):
        return self.plane_position

    def get_dry_crops(self):
        return self.dry_crops

    def get_fertilized_crop(self):
        return self.fertilized_crop

    def get_fertilized_crops(self):
        return self.fertilized_crops

    # ==========================================
    # NUEVOS MÉTODOS
    # ==========================================

    def get_plane_boarded(self):
        return self.plane_boarded

    def get_fuel_remaining(self):
        return self.fuel_remaining

    def get_cost(self):
        return self.cost

    def get_depth(self):
        return self.depth

    # ==========================================
    # IDENTIFICAR UN ESTADO
    # ==========================================

    def get_state_key(self):
        """
        Devuelve una representación inmutable
        de las variables relevantes del estado.

        No incluye costo, profundidad ni padre.
        """

        return (
            self.agro_bot_position,
            self.fertilizer_amount,
            frozenset(self.fertilized_crops),
            self.plane_boarded,
            self.fuel_remaining
        )


# ==============================================
# MOVIMIENTOS DISPONIBLES
# ==============================================

def get_next_possible_operators(node: Node):

    matrix = node.get_matrix()

    bot_row, bot_col = node.get_bot_pos()

    rows = len(matrix)
    cols = len(matrix[0])

    possible_operators = []

    # ------------------------------------------
    # ARRIBA
    # ------------------------------------------

    if (
        bot_row + 1 < rows
        and matrix[bot_row + 1][bot_col] != 1
    ):

        possible_operators.append(
            AgroBotOperators.UP
        )

    # ------------------------------------------
    # DERECHA
    # ------------------------------------------

    if (
        bot_col + 1 < cols
        and matrix[bot_row][bot_col + 1] != 1
    ):

        possible_operators.append(
            AgroBotOperators.RIGHT
        )

    # ------------------------------------------
    # ABAJO
    # ------------------------------------------

    if (
        bot_row - 1 >= 0
        and matrix[bot_row - 1][bot_col] != 1
    ):

        possible_operators.append(
            AgroBotOperators.DOWN
        )

    # ------------------------------------------
    # IZQUIERDA
    # ------------------------------------------

    if (
        bot_col - 1 >= 0
        and matrix[bot_row][bot_col - 1] != 1
    ):

        possible_operators.append(
            AgroBotOperators.LEFT
        )

    return possible_operators