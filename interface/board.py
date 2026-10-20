from pathlib import Path

import pygame


# ==========================================
# CONFIGURACIÓN
# ==========================================

ASSETS_DIR = Path(__file__).resolve().parent / "assets"

COLORS = {
    "free": (232, 242, 225),
    "wall": (85, 98, 93),
    "robot": (220, 236, 249),
    "crop": (250, 237, 207),
    "fertilizer": (218, 242, 223),
    "plane": (236, 225, 249),
    "treated": (210, 239, 207),
    "grid": (203, 218, 198),
    "text": (70, 85, 80),
    "robot_border": (65, 139, 210),
    "plane_border": (156, 116, 200),
}


# ==========================================
# COLORES DE LAS CASILLAS
# ==========================================

CELL_COLORS = {
    0: COLORS["free"],
    1: COLORS["wall"],
    2: COLORS["robot"],
    3: COLORS["crop"],
    4: COLORS["fertilizer"],
    5: COLORS["plane"],
    6: COLORS["treated"],
}


# ==========================================
# ARCHIVOS DE IMÁGENES
# ==========================================

IMAGE_FILES = {
    2: "robot.png",
    3: "cultivo_seco.png",
    4: "fertilizante.png",
    5: "avioneta.png",
    6: "cultivo.png",
}


# ==========================================
# SÍMBOLOS ALTERNATIVOS
# ==========================================

CELL_SYMBOLS = {
    2: "R",
    3: "C",
    4: "F",
    5: "A",
    6: "T",
}


# ==========================================
# ALMACENAMIENTO DE IMÁGENES
# ==========================================

SPRITES = {}
SCALED_SPRITES = {}


# ==========================================
# CARGAR IMÁGENES
# ==========================================

def load_sprites():
    """
    Carga las imágenes PNG desde assets.
    """

    SPRITES.clear()
    SCALED_SPRITES.clear()

    for value, filename in IMAGE_FILES.items():

        image_path = ASSETS_DIR / filename

        if not image_path.exists():

            print(
                f"Imagen no encontrada: {filename}"
            )

            continue

        try:

            image = pygame.image.load(
                str(image_path)
            ).convert_alpha()

            SPRITES[value] = image

        except pygame.error as error:

            print(
                f"Error al cargar {filename}: {error}"
            )


# ==========================================
# OBTENER IMAGEN ESCALADA
# ==========================================

def get_scaled_sprite(value, size):
    """
    Devuelve una imagen ajustada al tamaño
    de la casilla, conservando su proporción.
    """

    if value not in SPRITES:
        return None

    key = (value, size)

    if key in SCALED_SPRITES:
        return SCALED_SPRITES[key]

    original = SPRITES[value]

    width, height = original.get_size()

    scale = min(
        size / width,
        size / height
    )

    new_width = max(
        1,
        int(width * scale)
    )

    new_height = max(
        1,
        int(height * scale)
    )

    sprite = pygame.transform.smoothscale(
        original,
        (new_width, new_height)
    )

    SCALED_SPRITES[key] = sprite

    return sprite


# ==========================================
# DIBUJAR UNA IMAGEN
# ==========================================

def draw_element(screen, value, rect, font):
    """
    Dibuja el PNG del elemento.

    Si falta su imagen, utiliza una letra.
    """

    image_size = max(
        1,
        int(rect.width * 0.82)
    )

    sprite = get_scaled_sprite(
        value,
        image_size
    )

    if sprite is not None:

        image_rect = sprite.get_rect(
            center=rect.center
        )

        screen.blit(
            sprite,
            image_rect
        )

    else:

        symbol = CELL_SYMBOLS.get(value)

        if symbol is None:
            return

        text = font.render(
            symbol,
            True,
            COLORS["text"]
        )

        text_rect = text.get_rect(
            center=rect.center
        )

        screen.blit(
            text,
            text_rect
        )


# ==========================================
# IDENTIFICAR SI ESTÁ USANDO AVIONETA
# ==========================================

def is_using_plane(node):
    """
    La avioneta se muestra únicamente
    después de abordarla y mientras
    quede combustible.

    Cuando el combustible llega a cero,
    vuelve a mostrarse AgroBot.
    """

    if node is None:
        return False

    return (
        node.get_plane_boarded()
        and node.get_fuel_remaining() > 0
    )


# ==========================================
# RECONSTRUIR TERRENO
# ==========================================

def build_terrain(matrix, node=None):
    """
    Reconstruye la capa del terreno
    sin modificar la matriz del nodo.

    La avioneta:
        - Aparece antes del abordaje.
        - Desaparece de su posición inicial
          cuando el robot la aborda.
        - No vuelve a aparecer después
          de agotarse el combustible.
    """

    terrain = [
        row.copy()
        for row in matrix
    ]

    if node is None:
        return terrain

    # --------------------------------------
    # ELIMINAR ROBOT DE LA CAPA DEL TERRENO
    # --------------------------------------

    robot_row, robot_col = node.get_bot_pos()

    terrain[robot_row][robot_col] = 0

    # --------------------------------------
    # RESTAURAR DEPÓSITO DE FERTILIZANTE
    # --------------------------------------

    fertilizer_pos = node.get_fertilizer_pos()

    if fertilizer_pos is not None:

        row, col = fertilizer_pos

        terrain[row][col] = 4

    # --------------------------------------
    # MOSTRAR U OCULTAR AVIONETA ORIGINAL
    # --------------------------------------

    plane_pos = node.get_plane_pos()

    if plane_pos is not None:

        row, col = plane_pos

        if node.get_plane_boarded():

            # Ya fue utilizada.
            # No debe quedar otra avioneta
            # en la posición inicial.
            terrain[row][col] = 0

        else:

            # Todavía está disponible.
            terrain[row][col] = 5

    # --------------------------------------
    # REPRESENTAR CULTIVOS
    # --------------------------------------

    treated_crops = set(
        node.get_fertilized_crops()
    )

    for row, col in node.get_dry_crops():

        if (row, col) in treated_crops:

            terrain[row][col] = 6

        else:

            terrain[row][col] = 3

    return terrain


# ==========================================
# DIBUJAR TABLERO
# ==========================================

def draw_board(screen, matrix, area, node=None):
    """
    Dibuja el tablero mediante dos capas:

        1. Terreno y elementos.
        2. AgroBot o avioneta en movimiento.

    Cuando AgroBot aborda la avioneta,
    su imagen cambia automáticamente.

    Si se agota el combustible,
    se muestra nuevamente AgroBot.
    """

    terrain = build_terrain(
        matrix,
        node
    )

    rows = len(terrain)
    cols = len(terrain[0])

    available_width = area.width - 35
    available_height = area.height - 35

    cell_size = min(
        available_width // cols,
        available_height // rows
    )

    board_width = cols * cell_size
    board_height = rows * cell_size

    board_x = (
        area.x
        + (area.width - board_width) // 2
        + 10
    )

    board_y = (
        area.y
        + (area.height - board_height) // 2
        + 10
    )

    # --------------------------------------
    # FUENTES
    # --------------------------------------

    symbol_font = pygame.font.SysFont(
        "arial",
        max(16, cell_size // 2),
        bold=True
    )

    coordinate_font = pygame.font.SysFont(
        "arial",
        14
    )

    # ======================================
    # NÚMEROS DE COLUMNAS
    # ======================================

    for col in range(cols):

        text = coordinate_font.render(
            str(col),
            True,
            COLORS["text"]
        )

        x = (
            board_x
            + col * cell_size
            + cell_size // 2
        )

        screen.blit(
            text,
            text.get_rect(
                center=(x, board_y - 17)
            )
        )

    # ======================================
    # NÚMEROS DE FILAS
    # ======================================

    for row in range(rows):

        text = coordinate_font.render(
            str(row),
            True,
            COLORS["text"]
        )

        y = (
            board_y
            + row * cell_size
            + cell_size // 2
        )

        screen.blit(
            text,
            text.get_rect(
                center=(board_x - 18, y)
            )
        )

    # ======================================
    # CAPA 1: TERRENO
    # ======================================

    for row in range(rows):

        for col in range(cols):

            value = terrain[row][col]

            x = board_x + col * cell_size
            y = board_y + row * cell_size

            rect = pygame.Rect(
                x + 2,
                y + 2,
                cell_size - 4,
                cell_size - 4
            )

            color = CELL_COLORS.get(
                value,
                COLORS["free"]
            )

            # Fondo de la casilla
            pygame.draw.rect(
                screen,
                color,
                rect,
                border_radius=6
            )

            # Borde de la casilla
            pygame.draw.rect(
                screen,
                COLORS["grid"],
                rect,
                width=1,
                border_radius=6
            )

            # Imagen del elemento
            if value in IMAGE_FILES:

                draw_element(
                    screen,
                    value,
                    rect,
                    symbol_font
                )

    # ======================================
    # CAPA 2: ROBOT O AVIONETA EN MOVIMIENTO
    # ======================================

    robot_row = None
    robot_col = None

    if node is not None:

        robot_row, robot_col = (
            node.get_bot_pos()
        )

    else:

        # Compatibilidad con matrices
        # que todavía se dibujen sin nodo.
        for row in range(rows):

            for col in range(cols):

                if matrix[row][col] == 2:

                    robot_row = row
                    robot_col = col

                    break

            if robot_row is not None:
                break

    # --------------------------------------
    # DIBUJAR ELEMENTO EN MOVIMIENTO
    # --------------------------------------

    if robot_row is not None:

        x = board_x + robot_col * cell_size
        y = board_y + robot_row * cell_size

        robot_rect = pygame.Rect(
            x + 2,
            y + 2,
            cell_size - 4,
            cell_size - 4
        )

        # ----------------------------------
        # COMPROBAR MODO DE MOVIMIENTO
        # ----------------------------------

        using_plane = is_using_plane(node)

        if using_plane:

            background_color = COLORS["plane"]

            border_color = COLORS["plane_border"]

            sprite_value = 5

        else:

            background_color = COLORS["robot"]

            border_color = COLORS["robot_border"]

            sprite_value = 2

        # ----------------------------------
        # DIBUJAR FONDO DEL AGENTE
        # ----------------------------------

        pygame.draw.rect(
            screen,
            background_color,
            robot_rect,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            border_color,
            robot_rect,
            width=2,
            border_radius=6
        )

        # ----------------------------------
        # DIBUJAR IMAGEN DEL AGENTE
        # ----------------------------------

        draw_element(
            screen,
            sprite_value,
            robot_rect,
            symbol_font
        )