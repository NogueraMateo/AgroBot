from pathlib import Path

from search.world import create_root_node


# Dimensiones del terreno
MATRIX_SIZE = 10

# Valores permitidos en el archivo TXT
VALID_VALUES = {0, 1, 2, 3, 4, 5}


def load_world(file_path):
    """
    Lee un archivo TXT, valida su contenido
    y devuelve el nodo inicial del mundo.
    """

    # Convertir la ruta recibida en un objeto Path
    path = Path(file_path)

    # Verificar que el archivo existe
    if not path.is_file():
        raise ValueError("El archivo seleccionado no existe.")

    # Leer el archivo
    with open(path, "r", encoding="utf-8-sig") as file:

        # Separar las filas y sus valores
        rows = [
            line.split()
            for line in file
            if line.strip()
        ]

    # Validar cantidad de filas
    if len(rows) != MATRIX_SIZE:
        raise ValueError(
            "El archivo debe contener exactamente 10 filas."
        )

    matrix = []

    # Recorrer cada fila
    for row_index, row in enumerate(rows):

        # Validar cantidad de columnas
        if len(row) != MATRIX_SIZE:
            raise ValueError(
                f"La fila {row_index + 1} debe tener 10 columnas."
            )

        try:
            # Convertir los valores a enteros
            numeric_row = [int(value) for value in row]

        except ValueError:
            raise ValueError(
                f"La fila {row_index + 1} contiene valores no numéricos."
            )

        # Validar valores permitidos
        for value in numeric_row:

            if value not in VALID_VALUES:
                raise ValueError(
                    f"Valor no permitido: {value}"
                )

        matrix.append(numeric_row)

    # Convertir la matriz en una lista de valores
    all_values = [
        value
        for row in matrix
        for value in row
    ]

    # Verificar que exista un único AgroBot
    if all_values.count(2) != 1:
        raise ValueError(
            "Debe existir exactamente un AgroBot (2)."
        )

    # Verificar que exista un único depósito
    if all_values.count(4) != 1:
        raise ValueError(
            "Debe existir exactamente un depósito (4)."
        )

    # Verificar que exista una única avioneta
    if all_values.count(5) != 1:
        raise ValueError(
            "Debe existir exactamente una avioneta (5)."
        )

    # Convertir los números a cadenas para
    # reutilizar create_root_node()
    file_lines = [
        [str(value) for value in row]
        for row in matrix
    ]

    # Crear el nodo inicial
    root_node = create_root_node(file_lines)

    return root_node