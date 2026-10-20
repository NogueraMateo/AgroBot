import pygame


class AgroBotAnimation:
    """
    Reproduce una secuencia de estados de AgroBot.

    Puede utilizar rutas generadas por UCS, BFS,
    DFS, búsqueda ávara o A*, siempre que
    devuelvan una lista ordenada de nodos.
    """

    def __init__(self, speed=400):

        # Milisegundos entre movimientos
        self.speed = speed

        # Ruta que se va a reproducir
        self.path = []

        # Índice del estado visible
        self.current_index = 0

        # Control de reproducción
        self.playing = False
        self.finished = False

        # Momento del último movimiento
        self.last_update = 0

    def load_path(self, path):
        """
        Carga una nueva ruta y prepara
        la animación desde el primer estado.
        """

        self.path = list(path)

        self.current_index = 0

        self.playing = False
        self.finished = False

        self.last_update = pygame.time.get_ticks()

    def start(self):
        """Inicia o reanuda la reproducción."""

        if not self.path:
            return

        if self.finished:
            self.current_index = 0
            self.finished = False

        self.playing = True
        self.last_update = pygame.time.get_ticks()

    def pause(self):
        """Pausa la reproducción."""

        self.playing = False

    def stop(self):
        """Detiene la reproducción y elimina la ruta."""

        self.path = []

        self.current_index = 0

        self.playing = False
        self.finished = False

        self.last_update = 0

    def reset(self):
        """Vuelve al primer estado de la ruta."""

        self.current_index = 0

        self.playing = False
        self.finished = False

        self.last_update = pygame.time.get_ticks()

    def update(self):
        """
        Avanza un movimiento cuando transcurre
        el tiempo correspondiente.

        No bloquea el ciclo principal de Pygame.
        """

        if not self.playing:
            return

        if not self.path:
            return

        now = pygame.time.get_ticks()

        if now - self.last_update < self.speed:
            return

        self.last_update = now

        if self.current_index < len(self.path) - 1:

            self.current_index += 1

        if self.current_index >= len(self.path) - 1:

            self.playing = False
            self.finished = True

    def get_current_node(self):
        """Devuelve el estado que debe verse en pantalla."""

        if not self.path:
            return None

        return self.path[self.current_index]

    def get_progress(self):
        """Devuelve los movimientos reproducidos y el total."""

        if not self.path:
            return 0, 0

        return self.current_index, len(self.path) - 1

    def set_speed(self, milliseconds):
        """Permite cambiar la velocidad posteriormente."""

        if milliseconds <= 0:
            raise ValueError(
                "La velocidad debe ser mayor que cero."
            )

        self.speed = milliseconds