from .operators import AgroBotOperators

class Node():
    
    def __init__(
        self, matrix: list[list[int]], 
        agro_bot_position: tuple[int, int], 
        fertilizer_position: tuple[int, int],
        plane_position: tuple[int, int],
        dry_crops:list[tuple[int,int]],
        fertilizer_amount: int = 0,
        fertilized_crop: bool = False,
        fertilized_crops: list[tuple[int, int]] = [],
        parent_node: Node = None
    ):
        
        self.matrix = matrix
        self.fertilizer_amount = fertilizer_amount
        self.fertilizer_position = fertilizer_position
        self.plane_position = plane_position
        self.agro_bot_position = agro_bot_position
        self.dry_crops = dry_crops
        self.fertilized_crop = fertilized_crop
        self.fertilized_crops = fertilized_crops
        self.parent_node = parent_node

    def __str__(self):
        return (f"""
            Node \n 
            AgroBot Position: ({self.agro_bot_position[0]},{self.agro_bot_position[1]}) \n 
            Dry Crops Positions: {self.dry_crops}
            Fertilized Crops : {self.fertilized_crops}
""")
        

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


def get_next_possible_operators(node: Node):

    matrix = node.get_matrix()

    bot_row, bot_col = node.agro_bot_position

    possible_operators = []

    # Move up
    if bot_row+1 >= 0 and bot_row+1 <=9 and matrix[bot_row+1][bot_col] != 1:
        possible_operators.append(AgroBotOperators.UP)

    # Move right
    if bot_col+1 >= 0 and bot_col+1 <=9 and matrix[bot_row][bot_col+1] != 1:
        possible_operators.append(AgroBotOperators.RIGHT)

    # Move down
    if bot_row-1 >= 0 and bot_row-1 <=9 and matrix[bot_row-1][bot_col] != 1:
        possible_operators.append(AgroBotOperators.DOWN)

    # Move left
    if bot_col-1 >= 0 and bot_col-1 <=9 and matrix[bot_row][bot_col-1] != 1:
        possible_operators.append(AgroBotOperators.LEFT)

    return possible_operators
