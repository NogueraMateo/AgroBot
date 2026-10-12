from pathlib import Path
import sys


BASE_DIR = Path(__file__).resolve().parent.parent

if __name__ == "__main__" and not __package__:
    sys.path.insert(0, str(BASE_DIR))

from search.bfs import breadth_search
from search.world import create_root_node


test_file_path = BASE_DIR / "test_files" / "Prueba1.txt"

def main():    
    file_lines = []
    with open(test_file_path) as file:
        for line in file.readlines():
            file_lines.append(line.replace(" ", ""))

    root_node = create_root_node(file_lines)

    print(root_node)

    breadth_search(root_node)

if __name__ == "__main__":
    main()
