RED = 0
BLACK = 1
def rotate_left(node):
    """
    Realiza una rotación a la izquierda en el nodo.
    
    Args:
        node: El nodo en el que se realizará la rotación

    Returns:
        El nuevo nodo raíz después de la rotación
    """
    right_child = node["right"]
    node["right"] = right_child["left"]
    right_child["left"] = node
    right_child["color"] = node["color"]
    change_color(node, RED)
    
    # Actualizar el tamaño de los subárboles
    right_child["size"] = node["size"]
    node["size"] = 1 + (node["left"]["size"] if node["left"] else 0) + (node["right"]["size"] if node["right"] else 0)
    
    return right_child
def rotate_right(node):
    """
    Realiza una rotación a la derecha en el nodo.
    
    Args:
        node: El nodo en el que se realizará la rotación

    Returns:
        El nuevo nodo raíz después de la rotación
    """
    left_child = node["left"]
    node["left"] = left_child["right"]
    left_child["right"] = node
    left_child["color"] = node["color"]
    change_color(node, RED)
    
    # Actualizar el tamaño de los subárboles
    left_child["size"] = node["size"]
    node["size"] = 1 + (node["left"]["size"] if node["left"] else 0) + (node["right"]["size"] if node["right"] else 0)
    
    return left_child
def flip_colors(node):
    """
    Cambia el color del nodo y de sus hijos.
    
    Args:
        node: El nodo cuyo color y el de sus hijos serán cambiados

    Returns:
        None
    """
    change_color(node, RED if node["color"] == BLACK else BLACK)
    if node["left"]:
        change_color(node["left"], BLACK if node["left"]["color"] == RED else RED)
    if node["right"]:
        change_color(node["right"], BLACK if node["right"]["color"] == RED else RED)

def insert_node(node, key, value):
    # Caso base: crear un nuevo nodo rojo si el nodo es None (hoja vacía)
    if node is None:
        return new_node(key, value, RED)

    # Insertar el nodo en la posición correcta (comportamiento de un BST)
    if key < get_key(node):
        node["left"] = insert_node(node["left"], key, value)
    elif key > get_key(node):
        node["right"] = insert_node(node["right"], key, value)
    else:
        # Si la clave ya existe, actualizar el valor
        node["value"] = value
        return node

    # Mantener las propiedades del árbol rojo-negro
    if is_red(node["right"]) and not is_red(node["left"]):
        node = rotate_left(node)
    if is_red(node["left"]) and is_red(node["left"]["left"]):
        node = rotate_right(node)
    if is_red(node["left"]) and is_red(node["right"]):
        flip_colors(node)

    # Actualizar el tamaño del subárbol
    node["size"] = 1 + (node["left"]["size"] if node["left"] else 0) + (node["right"]["size"] if node["right"] else 0)
    return node

def new_node(key, value, color=RED):
    """
    Crea un nuevo nodo para un árbol rojo-negro  y lo retorna.
    color:0 - rojo  color:1 - negro
    Args:
        value: El valor asociado a la llave
        key: la llave asociada a la pareja
        size: El tamaño del subarbol que cuelga de este nodo
        color: El color inicial del nodo

    Returns:
        Un nodo con la pareja <llave, valor>
    Raises:
        Exception
    """
    node = {
        "key": key,
        "value": value,
        "size": 1,
        "left": None,
        "right": None,
        "color": color,
        "type": "RBT",
    }

    return node


def is_red(my_node):
    """
    Informa si un nodo es rojo
    Args:
        my_node: El nodo a revisar

    Returns:
        True si el nodo es rojo, False de lo contrario
    Raises:
        Exception
    """
    return my_node["color"] == RED


def get_value(my_node):
    """Retorna el valor asociado a una pareja llave valor
    Args:
        my_node: El nodo con la pareja llave-valor
    Returns:
        El valor almacenado en el nodo
    Raises:
        Exception
    """
    value = None
    if my_node is not None:
        value = my_node["value"]
    return value


def get_key(my_node):
    """Retorna la llave asociado a una pareja llave valor
    Args:
        my_node: El nodo con la pareja llave-valor
    Returns:
        La llave almacenada en el nodo
    Raises:
        Exception
    """
    key = None
    if my_node is not None:
        key = my_node["key"]
    return key


def change_color(my_node, color):
    """Cambia el color de un nodo
    Args:
        my_node: El nodo a cambiar
        color: El nuevo color del nodo
    Returns:
        None
    Raises:
        Exception
    """
    my_node["color"] = color
