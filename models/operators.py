from enum import Enum

class AgroBotOperators(Enum):
    UP = "UP"
    RIGHT = "RIGHT"
    DOWN = "DOWN"
    LEFT = "LEFT"

# ==========================================
# DIRECCIONES DE MOVIMIENTO
# ==========================================

MOVEMENTS = {
    AgroBotOperators.UP: (1, 0),
    AgroBotOperators.DOWN: (-1, 0),
    AgroBotOperators.RIGHT: (0, 1),
    AgroBotOperators.LEFT: (0, -1),
}