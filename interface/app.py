import pygame

from pathlib import Path
from tkinter import Tk, filedialog

from search.file_loader import load_world

from search.search_manager import (
    execute_search,
    is_algorithm_available
)

from interface.board import (
    draw_board,
    load_sprites
)

from interface.animation import AgroBotAnimation


# ==================================================
# CONFIGURACIÓN GENERAL
# ==================================================

LOGICAL_WIDTH = 1200
LOGICAL_HEIGHT = 880

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 880

FPS = 60

BASE_DIR = Path(__file__).resolve().parent.parent

DEFAULT_WORLD = BASE_DIR / "test_files" / "Prueba1.txt"


# ==================================================
# COLORES
# ==================================================

COLORS = {
    "background": (255, 255, 255),
    "white": (255, 255, 255),
    "primary": (45, 113, 78),
    "primary_hover": (34, 92, 63),
    "secondary": (226, 235, 225),
    "text": (38, 56, 47),
    "muted": (105, 122, 111),
    "border": (215, 226, 216),
    "disabled": (161, 174, 164),
    "error": (180, 65, 65),
    "plane": (156, 116, 200),
}


# ==================================================
# ALGORITMOS
# ==================================================

SEARCH_ALGORITHMS = {
    "No informada": [
        "Amplitud",
        "Costo uniforme",
        "Profundidad evitando ciclos"
    ],
    "Informada": [
        "Avara",
        "A*"
    ]
}


# ==================================================
# FUNCIONES PARA DIBUJAR
# ==================================================

def draw_text(screen, text, x, y, font, color=None):

    if color is None:
        color = COLORS["text"]

    rendered = font.render(
        str(text),
        True,
        color
    )

    screen.blit(rendered, (x, y))


def draw_centered_text(screen, text, rect, font, color):

    rendered = font.render(
        str(text),
        True,
        color
    )

    text_rect = rendered.get_rect(
        center=rect.center
    )

    screen.blit(rendered, text_rect)


def draw_panel(screen, rect):

    pygame.draw.rect(
        screen,
        COLORS["white"],
        rect,
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        COLORS["border"],
        rect,
        width=1,
        border_radius=12
    )


def shorten_text(text, font, max_width):

    text = str(text)

    if font.size(text)[0] <= max_width:
        return text

    while text and font.size(text + "...")[0] > max_width:
        text = text[:-1]

    return text + "..."


def draw_button(
    screen,
    rect,
    text,
    font,
    mouse_pos,
    enabled=True,
    secondary=False
):

    if not enabled:
        color = COLORS["disabled"]

    elif secondary:
        color = COLORS["secondary"]

    elif rect.collidepoint(mouse_pos):
        color = COLORS["primary_hover"]

    else:
        color = COLORS["primary"]

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=8
    )

    text_color = (
        COLORS["text"]
        if secondary
        else COLORS["white"]
    )

    draw_centered_text(
        screen,
        text,
        rect,
        font,
        text_color
    )


def draw_stat(
    screen,
    label,
    value,
    x,
    label_y,
    value_y,
    label_font,
    value_font
):

    draw_text(
        screen,
        label,
        x,
        label_y,
        label_font,
        COLORS["muted"]
    )

    draw_text(
        screen,
        value,
        x,
        value_y,
        value_font,
        COLORS["primary"]
    )


# ==================================================
# SELECTOR DESPLEGABLE
# ==================================================

class Dropdown:

    def __init__(self, rect, options):

        self.rect = pygame.Rect(rect)

        self.options = list(options)

        self.selected = 0
        self.expanded = False

    def get_value(self):

        return self.options[self.selected]

    def set_options(self, options):

        self.options = list(options)

        self.selected = 0
        self.expanded = False

    def handle_click(self, pos):

        if self.rect.collidepoint(pos):

            self.expanded = not self.expanded
            return False

        if self.expanded:

            for index, option in enumerate(self.options):

                option_rect = pygame.Rect(
                    self.rect.x,
                    self.rect.bottom + index * self.rect.height,
                    self.rect.width,
                    self.rect.height
                )

                if option_rect.collidepoint(pos):

                    changed = index != self.selected

                    self.selected = index
                    self.expanded = False

                    return changed

        self.expanded = False
        return False

    def draw(self, screen, font):

        pygame.draw.rect(
            screen,
            COLORS["white"],
            self.rect,
            border_radius=7
        )

        pygame.draw.rect(
            screen,
            COLORS["border"],
            self.rect,
            width=1,
            border_radius=7
        )

        selected_text = shorten_text(
            self.get_value(),
            font,
            self.rect.width - 50
        )

        draw_text(
            screen,
            selected_text,
            self.rect.x + 12,
            self.rect.y + 10,
            font
        )

        draw_text(
            screen,
            "v",
            self.rect.right - 25,
            self.rect.y + 10,
            font,
            COLORS["muted"]
        )

    def draw_options(self, screen, font):

        if not self.expanded:
            return

        for index, option in enumerate(self.options):

            rect = pygame.Rect(
                self.rect.x,
                self.rect.bottom + index * self.rect.height,
                self.rect.width,
                self.rect.height
            )

            color = (
                COLORS["secondary"]
                if index == self.selected
                else COLORS["white"]
            )

            pygame.draw.rect(
                screen,
                color,
                rect
            )

            pygame.draw.rect(
                screen,
                COLORS["border"],
                rect,
                width=1
            )

            option_text = shorten_text(
                option,
                font,
                rect.width - 24
            )

            draw_text(
                screen,
                option_text,
                rect.x + 12,
                rect.y + 10,
                font
            )


# ==================================================
# SELECCIONAR ARCHIVO TXT
# ==================================================

def select_txt_file():

    root = Tk()
    root.withdraw()

    try:

        file_path = filedialog.askopenfilename(
            parent=root,
            title="Seleccionar mundo AgroBot",
            initialdir=str(BASE_DIR / "test_files"),
            filetypes=[
                ("Archivos TXT", "*.txt")
            ]
        )

    finally:

        root.destroy()

    return file_path


# ==================================================
# ESCALADO DE VENTANA
# ==================================================

def calculate_viewport(window_size):

    width, height = window_size

    scale = min(
        width / LOGICAL_WIDTH,
        height / LOGICAL_HEIGHT
    )

    scaled_width = max(
        1,
        int(LOGICAL_WIDTH * scale)
    )

    scaled_height = max(
        1,
        int(LOGICAL_HEIGHT * scale)
    )

    offset_x = (width - scaled_width) // 2
    offset_y = (height - scaled_height) // 2

    viewport = pygame.Rect(
        offset_x,
        offset_y,
        scaled_width,
        scaled_height
    )

    return scale, viewport


def convert_mouse_position(mouse_pos, viewport):

    if not viewport.collidepoint(mouse_pos):
        return (-1, -1)

    x = (
        (mouse_pos[0] - viewport.x)
        * LOGICAL_WIDTH
        / viewport.width
    )

    y = (
        (mouse_pos[1] - viewport.y)
        * LOGICAL_HEIGHT
        / viewport.height
    )

    return int(x), int(y)


# ==================================================
# APLICACIÓN PRINCIPAL
# ==================================================

def main():

    # ----------------------------------------------
    # INICIAR PYGAME
    # ----------------------------------------------

    pygame.init()

    screen = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT),
        pygame.RESIZABLE
    )

    pygame.display.set_caption(
        "AgroBot - Simulador de búsqueda inteligente"
    )

    # Cargar imágenes
    load_sprites()

    canvas = pygame.Surface(
        (LOGICAL_WIDTH, LOGICAL_HEIGHT)
    )

    clock = pygame.time.Clock()

    # ----------------------------------------------
    # CONTROLADOR DE ANIMACIÓN
    # ----------------------------------------------

    animation = AgroBotAnimation(speed=400)

    # ----------------------------------------------
    # FUENTES
    # ----------------------------------------------

    title_font = pygame.font.SysFont(
        "arial", 34, bold=True
    )

    section_font = pygame.font.SysFont(
        "arial", 19, bold=True
    )

    label_font = pygame.font.SysFont(
        "arial", 15, bold=True
    )

    text_font = pygame.font.SysFont(
        "arial", 16
    )

    small_font = pygame.font.SysFont(
        "arial", 13
    )

    value_font = pygame.font.SysFont(
        "arial", 23, bold=True
    )

    # ----------------------------------------------
    # CARGAR MUNDO INICIAL
    # ----------------------------------------------

    root_node = None
    current_file = "Ninguno"

    message = "Selecciona un archivo TXT"
    message_is_error = False

    try:

        root_node = load_world(DEFAULT_WORLD)

        current_file = DEFAULT_WORLD.name

        message = "Mundo cargado correctamente"

    except (ValueError, OSError) as error:

        message = str(error)
        message_is_error = True

    # ----------------------------------------------
    # PANELES
    # ----------------------------------------------

    board_panel = pygame.Rect(
        24, 118, 700, 700
    )

    control_panel = pygame.Rect(
        740, 118, 435, 440
    )

    status_panel = pygame.Rect(
        740, 570, 435, 102
    )

    results_panel = pygame.Rect(
        740, 684, 435, 134
    )

    board_area = pygame.Rect(
        50, 190, 650, 540
    )

    # ----------------------------------------------
    # BOTONES
    # ----------------------------------------------

    load_button = pygame.Rect(
        760, 229, 395, 40
    )

    start_button = pygame.Rect(
        760, 429, 395, 40
    )

    reset_button = pygame.Rect(
        760, 478, 395, 40
    )

    # ----------------------------------------------
    # SELECTORES
    # ----------------------------------------------

    search_type_dropdown = Dropdown(
        (760, 304, 395, 38),
        list(SEARCH_ALGORITHMS.keys())
    )

    algorithm_dropdown = Dropdown(
        (760, 376, 395, 38),
        SEARCH_ALGORITHMS["No informada"]
    )

    # ----------------------------------------------
    # ESTADÍSTICAS INICIALES
    # ----------------------------------------------

    expanded_nodes = "--"
    depth = "--"
    solution_cost = "--"
    execution_time = "--"

    search_result = None

    # ----------------------------------------------
    # PANTALLA COMPLETA
    # ----------------------------------------------

    fullscreen = False

    previous_window_size = (
        WINDOW_WIDTH,
        WINDOW_HEIGHT
    )

    # ----------------------------------------------
    # CICLO PRINCIPAL
    # ----------------------------------------------

    running = True

    while running:

        _, viewport = calculate_viewport(
            screen.get_size()
        )

        mouse_pos = convert_mouse_position(
            pygame.mouse.get_pos(),
            viewport
        )

        # ==========================================
        # EVENTOS
        # ==========================================

        for event in pygame.event.get():

            # --------------------------------------
            # CERRAR APLICACIÓN
            # --------------------------------------

            if event.type == pygame.QUIT:

                running = False

            # --------------------------------------
            # TECLADO: PANTALLA COMPLETA
            # --------------------------------------

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_F11:

                    fullscreen = not fullscreen

                    if fullscreen:

                        previous_window_size = screen.get_size()

                        screen = pygame.display.set_mode(
                            (0, 0),
                            pygame.FULLSCREEN
                        )

                    else:

                        screen = pygame.display.set_mode(
                            previous_window_size,
                            pygame.RESIZABLE
                        )

            # --------------------------------------
            # CLICS DEL MOUSE
            # --------------------------------------

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button != 1:
                    continue

                click_pos = convert_mouse_position(
                    event.pos,
                    viewport
                )

                # ==================================
                # SELECTORES
                # ==================================

                if algorithm_dropdown.expanded:

                    algorithm_dropdown.handle_click(
                        click_pos
                    )

                    search_type_dropdown.expanded = False

                    continue

                if search_type_dropdown.expanded:

                    changed = search_type_dropdown.handle_click(
                        click_pos
                    )

                    if changed:

                        search_type = (
                            search_type_dropdown.get_value()
                        )

                        algorithm_dropdown.set_options(
                            SEARCH_ALGORITHMS[search_type]
                        )

                    algorithm_dropdown.expanded = False

                    continue

                if search_type_dropdown.rect.collidepoint(
                    click_pos
                ):

                    search_type_dropdown.handle_click(
                        click_pos
                    )

                    continue

                if algorithm_dropdown.rect.collidepoint(
                    click_pos
                ):

                    algorithm_dropdown.handle_click(
                        click_pos
                    )

                    continue

                # ==================================
                # CARGAR ARCHIVO TXT
                # ==================================

                if load_button.collidepoint(click_pos):

                    file_path = select_txt_file()

                    if file_path:

                        try:

                            new_root = load_world(file_path)

                            # Actualizar mundo
                            root_node = new_root
                            current_file = Path(file_path).name

                            # Detener animación anterior
                            animation.stop()

                            # Limpiar resultados
                            search_result = None

                            expanded_nodes = "--"
                            depth = "--"
                            solution_cost = "--"
                            execution_time = "--"

                            message = "Mundo cargado correctamente"
                            message_is_error = False

                        except (ValueError, OSError) as error:

                            message = str(error)
                            message_is_error = True

                # ==================================
                # REINICIAR
                # ==================================

                elif reset_button.collidepoint(click_pos):

                    if root_node is not None:

                        animation.stop()

                        search_result = None

                        expanded_nodes = "--"
                        depth = "--"
                        solution_cost = "--"
                        execution_time = "--"

                        message = "Estado inicial restaurado"
                        message_is_error = False

                # ==================================
                # INICIAR BÚSQUEDA
                # ==================================

                elif start_button.collidepoint(click_pos):

                    if root_node is None:

                        message = "Primero debes cargar un mundo."
                        message_is_error = True

                    else:

                        # Obtener opciones seleccionadas
                        search_type = (
                            search_type_dropdown.get_value()
                        )

                        algorithm_name = (
                            algorithm_dropdown.get_value()
                        )

                        # Verificar disponibilidad
                        available = is_algorithm_available(
                            search_type,
                            algorithm_name
                        )

                        if not available:

                            message = (
                                f"El algoritmo '{algorithm_name}' "
                                "todavía no está disponible."
                            )

                            message_is_error = True

                        else:

                            animation.stop()
                            search_result = None

                            expanded_nodes = "--"
                            depth = "--"
                            solution_cost = "--"
                            execution_time = "--"

                            message = f"Ejecutando {algorithm_name}..."
                            message_is_error = False

                            try:

                                # Ejecutar algoritmo seleccionado
                                result = execute_search(
                                    search_type,
                                    algorithm_name,
                                    root_node
                                )

                                # Comprobar campos necesarios
                                required_keys = (
                                    "found",
                                    "path",
                                    "cost",
                                    "expanded_nodes",
                                    "depth",
                                    "execution_time",
                                    "status"
                                )

                                missing_keys = [
                                    key
                                    for key in required_keys
                                    if key not in result
                                ]

                                if missing_keys:

                                    raise ValueError(
                                        "El algoritmo no devolvió "
                                        "todos los campos requeridos: "
                                        + ", ".join(missing_keys)
                                    )

                                search_result = result

                                # ----------------------------------
                                # ESTADÍSTICAS
                                # ----------------------------------

                                expanded_nodes = str(
                                    result["expanded_nodes"]
                                )

                                depth = (
                                    str(result["depth"])
                                    if result["depth"] is not None
                                    else "--"
                                )

                                solution_cost = (
                                    f'{result["cost"]:.1f}'
                                    if result["cost"] is not None
                                    else "--"
                                )

                                execution_time = (
                                    f'{result["execution_time"]:.3f} s'
                                )

                                # ----------------------------------
                                # ANIMACIÓN
                                # ----------------------------------

                                if result["found"] and result["path"]:

                                    animation.load_path(
                                        result["path"]
                                    )

                                    animation.start()

                                    message = (
                                        f"{algorithm_name}: "
                                        "solución encontrada. "
                                        "Reproduciendo ruta..."
                                    )

                                    message_is_error = False

                                else:

                                    message = result["status"]
                                    message_is_error = not result["found"]

                            except (
                                NotImplementedError,
                                ValueError,
                                KeyError,
                                TypeError
                            ) as error:

                                animation.stop()
                                search_result = None

                                message = (
                                    f"Error en {algorithm_name}: "
                                    f"{error}"
                                )

                                message_is_error = True

        # ==========================================
        # ACTUALIZAR ANIMACIÓN
        # ==========================================

        animation.update()

        current_node = animation.get_current_node()

        if current_node is None:
            current_node = root_node

        if animation.finished:

            animation.finished = False

            message = "Animación finalizada."
            message_is_error = False

        # ==========================================
        # OBTENER ESTADO ACTUAL DEL ROBOT
        # ==========================================

        fertilizer = 0
        fuel = 30
        treated_crops = 0
        total_crops = 0

        if root_node is not None:

            total_crops = len(
                root_node.get_dry_crops()
            )

        if current_node is not None:

            fertilizer = (
                current_node.get_fertilizer_amount()
            )

            fuel = (
                current_node.get_fuel_remaining()
            )

            treated_crops = len(
                current_node.get_fertilized_crops()
            )

        # ==========================================
        # IDENTIFICAR MODO DE TRANSPORTE
        # ==========================================

        transport_status = "Modo: AgroBot"

        if current_node is not None:

            if (
                current_node.get_plane_boarded()
                and current_node.get_fuel_remaining() > 0
            ):

                transport_status = "Modo: Avioneta"

            elif (
                current_node.get_plane_boarded()
                and current_node.get_fuel_remaining() == 0
            ):

                transport_status = "Modo: AgroBot"

        # ==========================================
        # DIBUJAR FONDO
        # ==========================================

        canvas.fill(
            COLORS["background"]
        )

        # ==========================================
        # ENCABEZADO
        # ==========================================

        draw_text(
            canvas,
            "AGROBOT",
            35,
            25,
            title_font,
            COLORS["primary"]
        )

        draw_text(
            canvas,
            "Simulador de búsqueda inteligente",
            37,
            70,
            text_font,
            COLORS["muted"]
        )

        # ==========================================
        # PANELES
        # ==========================================

        draw_panel(canvas, board_panel)
        draw_panel(canvas, control_panel)
        draw_panel(canvas, status_panel)
        draw_panel(canvas, results_panel)

        # ==========================================
        # TERRENO DE CULTIVO
        # ==========================================

        draw_text(
            canvas,
            "TERRENO DE CULTIVO",
            48,
            140,
            section_font
        )

        if current_node is not None:

            draw_board(
                canvas,
                current_node.get_matrix(),
                board_area,
                node=current_node
            )

        # ==========================================
        # LEYENDA
        # ==========================================

        legend_items = [
            ("AgroBot", (65, 139, 210), 55, 745),
            ("Obstáculo", (85, 98, 93), 200, 745),
            ("Cultivo seco", (224, 166, 74), 355, 745),
            ("Fertilizante", (65, 158, 103), 55, 772),
            ("Avioneta", (156, 116, 200), 220, 772),
        ]

        for name, color, x, y in legend_items:

            pygame.draw.rect(
                canvas,
                color,
                pygame.Rect(x, y + 1, 15, 15),
                border_radius=3
            )

            draw_text(
                canvas,
                name,
                x + 23,
                y,
                small_font
            )

        # ==========================================
        # PANEL DE CONTROL
        # ==========================================

        draw_text(
            canvas,
            "PANEL DE CONTROL",
            760,
            137,
            section_font
        )

        draw_text(
            canvas,
            "ARCHIVO DEL MUNDO",
            760,
            178,
            label_font
        )

        file_name = shorten_text(
            current_file,
            text_font,
            380
        )

        draw_text(
            canvas,
            file_name,
            760,
            201,
            text_font,
            COLORS["muted"]
        )

        draw_button(
            canvas,
            load_button,
            "Cargar archivo TXT",
            label_font,
            mouse_pos
        )

        draw_text(
            canvas,
            "TIPO DE BÚSQUEDA",
            760,
            281,
            label_font
        )

        draw_text(
            canvas,
            "ALGORITMO",
            760,
            353,
            label_font
        )

        draw_button(
            canvas,
            start_button,
            "Iniciar búsqueda",
            label_font,
            mouse_pos,
            enabled=root_node is not None
        )

        draw_button(
            canvas,
            reset_button,
            "Reiniciar",
            label_font,
            mouse_pos,
            secondary=True
        )

        draw_text(
            canvas,
            "Selecciona un algoritmo y presiona Iniciar búsqueda.",
            760,
            528,
            small_font,
            COLORS["muted"]
        )

        # ==========================================
        # ESTADO DEL ROBOT
        # ==========================================

        draw_text(
            canvas,
            "ESTADO DEL ROBOT",
            760,
            585,
            section_font
        )

        # Indicador del modo de transporte
        transport_color = (
            COLORS["plane"]
            if transport_status == "Modo: Avioneta"
            else COLORS["primary"]
        )

        draw_text(
            canvas,
            transport_status,
            1010,
            590,
            small_font,
            transport_color
        )

        draw_stat(
            canvas,
            "Fertilizante",
            f"{fertilizer}/2",
            760,
            619,
            638,
            small_font,
            value_font
        )

        draw_stat(
            canvas,
            "Combustible",
            f"{fuel}/30",
            895,
            619,
            638,
            small_font,
            value_font
        )

        draw_stat(
            canvas,
            "Cultivos tratados",
            f"{treated_crops}/{total_crops}",
            1030,
            619,
            638,
            small_font,
            value_font
        )

        # ==========================================
        # RESULTADOS DE BÚSQUEDA
        # ==========================================

        draw_text(
            canvas,
            "RESULTADOS DE BÚSQUEDA",
            760,
            699,
            section_font
        )

        draw_stat(
            canvas,
            "Nodos expandidos",
            expanded_nodes,
            760,
            733,
            753,
            small_font,
            value_font
        )

        draw_stat(
            canvas,
            "Profundidad",
            depth,
            875,
            733,
            753,
            small_font,
            value_font
        )

        draw_stat(
            canvas,
            "Costo",
            solution_cost,
            975,
            733,
            753,
            small_font,
            value_font
        )

        draw_stat(
            canvas,
            "Tiempo",
            execution_time,
            1080,
            733,
            753,
            small_font,
            value_font
        )

        # ==========================================
        # SELECTORES DESPLEGABLES
        # ==========================================

        search_type_dropdown.draw(
            canvas,
            text_font
        )

        algorithm_dropdown.draw(
            canvas,
            text_font
        )

        search_type_dropdown.draw_options(
            canvas,
            text_font
        )

        algorithm_dropdown.draw_options(
            canvas,
            text_font
        )

        # ==========================================
        # MENSAJE DE ESTADO
        # ==========================================

        message_color = (
            COLORS["error"]
            if message_is_error
            else COLORS["primary"]
        )

        display_message = shorten_text(
            message,
            small_font,
            900
        )

        draw_text(
            canvas,
            display_message,
            35,
            840,
            small_font,
            message_color
        )

        # ==========================================
        # ADAPTAR A LA VENTANA
        # ==========================================

        screen.fill(
            COLORS["background"]
        )

        _, viewport = calculate_viewport(
            screen.get_size()
        )

        scaled_canvas = pygame.transform.smoothscale(
            canvas,
            viewport.size
        )

        screen.blit(
            scaled_canvas,
            viewport.topleft
        )

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


# ==================================================
# EJECUTAR
# ==================================================

if __name__ == "__main__":
    main()