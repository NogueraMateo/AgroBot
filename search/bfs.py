from queue import Queue

from models.node import Node, get_next_possible_operators
from models.operators import AgroBotOperators
from search.helpers import get_next_move_node, is_node_the_goal


def is_cicle(node: Node) -> bool:
    parent = node.parent_node

    while parent is not None:
        if (parent.get_bot_pos() == node.get_bot_pos()
            and parent.get_fertilizer_amount() == node.get_fertilizer_amount()
            and parent.get_fertilized_crops() == node.get_fertilized_crops()
            ):
            return True

        parent = parent.parent_node

    return False
    

def breadth_search(root: Node):

    queue = Queue()

    queue.put(root)

    while True:
        if queue.empty():
            print("Busqueda fallida terminando algoritmo..")
            break

        node:Node = queue.get()

        if is_node_the_goal(node):
            print("Solución encontrada")
            print(node)
            for row in node.get_matrix():
                print(row)
            return True

        next_ops = get_next_possible_operators(node)
        matrix = node.get_matrix()

        next_row = next_col = None
        for op in next_ops:
            match op:
                case AgroBotOperators.UP:
                    next_row = node.get_bot_pos()[0] + 1
                    next_col = node.get_bot_pos()[1]
                    
                case AgroBotOperators.RIGHT:
                    next_row = node.get_bot_pos()[0]
                    next_col = node.get_bot_pos()[1] + 1

                case AgroBotOperators.DOWN:
                    next_row = node.get_bot_pos()[0] - 1
                    next_col = node.get_bot_pos()[1] 
                case AgroBotOperators.LEFT:
                    next_row = node.get_bot_pos()[0]
                    next_col = node.get_bot_pos()[1] - 1

            next_possible_node = get_next_move_node(
                                    matrix,
                                    next_row,
                                    next_col,
                                    node
                                )
            
            if is_cicle(next_possible_node):
                continue
                                
            queue.put(next_possible_node)