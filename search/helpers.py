from models.node import Node
import copy

def is_node_the_goal(node: Node):
    node_matrix = node.get_matrix()
    dry_crops = node.dry_crops

    for row, col in dry_crops: 
        if (
            node_matrix[row][col] != 6 and 
            not (node_matrix[row][col] == 2 and node.get_fertilized_crop())):
            return False

    return True


def get_next_move_node(matrix: list[list[int]], next_row: int, next_col: int, prev_node: Node):
    next_cell_val = matrix[next_row][next_col]
    fertilizer_amount = prev_node.get_fertilizer_amount()
    fertilized_crop = False
    fertilized_crops = copy.deepcopy(prev_node.get_fertilized_crops()) 

    match next_cell_val:
                    
        case 3:
            # If the next cell is a dry crop then mark it as fertilized and decrease 
            # fertilizer amount by one

            if fertilizer_amount > 0 and not (next_row, next_col) in fertilized_crops:
                fertilized_crop = True
                fertilizer_amount -= 1
                fertilized_crops.append((next_row, next_col))


        case 4:
            # If the next cell is a fertilizer tank then refill the tank no matter what

            fertilizer_amount = 2

    new_matrix = copy.deepcopy(matrix)

    # Before moving the Agro bot to the next cell make sure the previous cell is filled
    # with the original object, either empty cell, tank, dry crop, plane or not dry crop.
    prev_bot_pos = prev_node.get_bot_pos()

    if prev_bot_pos == prev_node.get_fertilizer_pos():
        new_matrix[prev_bot_pos[0]][prev_bot_pos[1]] = 4
    elif prev_bot_pos == prev_node.get_plane_pos():
        new_matrix[prev_bot_pos[0]][prev_bot_pos[1]] = 5
    elif prev_bot_pos in prev_node.get_dry_crops():
        if prev_node.get_fertilized_crop():
            new_matrix[prev_bot_pos[0]][prev_bot_pos[1]] = 6
        else:
            new_matrix[prev_bot_pos[0]][prev_bot_pos[1]] = 3
    else:
        new_matrix[prev_bot_pos[0]][prev_bot_pos[1]] = 0

    # Now move the agro bot to the next cell
    new_matrix[next_row][next_col] = 2

    return Node(
        new_matrix, 
        (next_row, next_col), 
        prev_node.get_fertilizer_pos(), 
        prev_node.get_plane_pos(), 
        prev_node.get_dry_crops(), 
        fertilizer_amount, 
        fertilized_crop,
        fertilized_crops,
        prev_node
    )