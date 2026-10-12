from models.node import Node

# ===============================
# GAME RULES
# ===============================

"""
GAME CONVENTIONS

0 for free cell
1 for obstacle
2 for AgroBot
3 for dry crop
4 for fertilizer tank
5 for the plane
6 for not dry crops
"""

MATRIX_DIM = 10


def create_root_node(file_lines: list[str]) ->list[list[int]]:

    matrix = [[0 for _ in range(MATRIX_DIM)] for _ in range(MATRIX_DIM)]
    dry_crops = []
    
    cell_value = agro_bot_pos = fertilizer_pos = plane_pos = None
    for i in range(MATRIX_DIM):
        
        for j in range(MATRIX_DIM):

            cell_value = int(file_lines[i][j])
            
            if cell_value == 3: dry_crops.append((i,j))
            elif cell_value == 2: agro_bot_pos = (i,j)
            elif cell_value == 4: fertilizer_pos = (i,j)
            elif cell_value == 5: plane_pos = (i,j)

            matrix[i][j] = cell_value

    return Node(matrix, agro_bot_pos, fertilizer_pos, plane_pos, dry_crops)
