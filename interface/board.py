import pygame

from pathlib import Path


# ==========================================
# RUTA DE LAS IMÁGENES
# ==========================================

ASSETS_DIR = Path(__file__).resolve().parent / "assets"


# ==========================================
# COLORES
# ==========================================

COLORS = {
    "free": (232, 242, 225),
    "wall": (85, 98, 93),
    "robot": (220, 236, 249),
    "crop": (250, 237, 207),
    "fertilizer": (218, 242, 223),
    "plane": (236, 225, 249),
    "treated": (210, 239, 207),
    "grid": (203, 218, 198),
    "white": (255, 255, 255),
    "text": (70, 85, 80),
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


# Símbolos alternativos si falta una imagen
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
    Carga las imágenes de los elementos
    del mundo una sola vez.
    """

    for value, filename in IMAGE_FILES.items():

        image_path = ASSETS_DIR / filename

        if image_path.exists():

            try:

                image = pygame.image.load(
                    str(image_path)
                ).convert_alpha()

                SPRITES[value] = image

            except pygame.error as error:

                print(
                    f"Error al cargar {filename}: {error}"
                )

        else:

            print(
                f"Imagen no encontrada: {filename}"
            )


# ==========================================
# OBTENER IMAGEN ESCALADA
# ==========================================

def get_scaled_sprite(value, size):
    """
    Devuelve una imagen adaptada al
    tamaño de la casilla.
    """

    if value not in SPRITES:
        return None

    key = (value, size)

    # Reutilizar imagen si ya fue escalada
    if key in SCALED_SPRITES:

        return SCALED_SPRITES[key]

    original_image = SPRITES[value]

    # Mantener proporción de la imagen
    width, height = original_image.get_size()

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

    scaled_image = pygame.transform.smoothscale(
        original_image,
        (new_width, new_height)
    )

    SCALED_SPRITES[key] = scaled_image

    return scaled_image


# ==========================================
# DIBUJAR ELEMENTO
# ==========================================

def draw_element(
    screen,
    value,
    rect,
    symbol_font
):
    """
    Dibuja una imagen en la casilla.

    Si no existe la imagen, utiliza
    una letra como alternativa.
    """

    # Dejar un margen dentro de la casilla
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

        if symbol:

            text = symbol_font.render(
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
# DIBUJAR TABLERO
# ==========================================

def draw_board(screen, matrix, area):
    """
    Dibuja el mundo AgroBot
    utilizando imágenes PNG.
    """

    rows = len(matrix)
    cols = len(matrix[0])

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

    # Fuentes
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
    # COORDENADAS DE COLUMNAS
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

        text_rect = text.get_rect(
            center=(x, board_y - 17)
        )

        screen.blit(text, text_rect)

    # ======================================
    # COORDENADAS DE FILAS
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

        text_rect = text.get_rect(
            center=(board_x - 18, y)
        )

        screen.blit(text, text_rect)

    # ======================================
    # CASILLAS
    # ======================================

    for row in range(rows):

        for col in range(cols):

            value = matrix[row][col]

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

            # Fondo de casilla
            pygame.draw.rect(
                screen,
                color,
                rect,
                border_radius=6
            )

            # Borde
            pygame.draw.rect(
                screen,
                COLORS["grid"],
                rect,
                width=1,
                border_radius=6
            )

            # Dibujar imagen
            if value in IMAGE_FILES:

                draw_element(
                    screen,
                    value,
                    rect,
                    symbol_font
                )