import random
import constants
from utils import get_coords

def initialize_board():
    board = [[" " for _ in range(constants.GRID_WIDTH)] for _ in range(constants.GRID_HEIGHT)]
    return board

def can_place_ship(board, row, col, size, orientation):
    height = len(board)
    width = len(board[0])
    orientation = orientation.upper()
    
    if orientation == 'H':
        if col + size > width:
            return False
        for c in range(col, col + size):
            if board[row][c] != " ":
                return False
    elif orientation == 'V':
        if row + size > height:
            return False
        for r in range(row, row + size):
            if board[r][col] != " ":
                return False
    else:
        return False
        
    return True

def place_ship(board, row, col, size, orientation):
    orientation = orientation.upper()
    if orientation == 'H':
        for c in range(col, col + size):
            board[row][c] = "S"
    elif orientation == 'V':
        for r in range(row, row + size):
            board[r][col] = "S"

def place_ships_randomly(board):
    height = len(board)
    width = len(board[0])
    
    for ship_name, size in constants.SHIP_SIZES.items():
        placed = False
        attempts = 0
        while not placed and attempts < 1000:
            orientation = random.choice(['H', 'V'])
            row = random.randint(0, height - 1)
            col = random.randint(0, width - 1)
            
            if can_place_ship(board, row, col, size, orientation):
                place_ship(board, row, col, size, orientation)
                placed = True
            attempts += 1
        if not placed:
            raise RuntimeError(f"No se pudo colocar el barco '{ship_name}' de tamaño {size} después de 1000 intentos.")

def handle_shot(board, row, col):
    """
    Procesa un disparo en el tablero del oponente.
    Retorna una tupla (validez_disparo, mensaje).
    """
    height = len(board)
    width = len(board[0])
    
    if row < 0 or row >= height or col < 0 or col >= width:
        return False, "Coordenadas fuera del tablero."
        
    cell = board[row][col]
    if cell == "X" or cell == "-":
        return False, "Ya has disparado en esta coordenada anteriormente."
        
    if cell == "S":
        board[row][col] = "X"
        return True, "¡TOCADO!"
    else:
        board[row][col] = "-"
        return True, "Agua..."

def has_ships_remaining(board):
    """
    Devuelve True si aún queda algún barco ("S") intacto en el tablero.
    """
    for row in board:
        if "S" in row:
            return True
    return False

def print_board(board, hide_ships=False):
    """
    Genera y muestra el tablero visual con etiquetas de filas (letras) y columnas (números).
    Si hide_ships es True, oculta los barcos ("S") reemplazándolos con espacios vacíos.
    """
    width = len(constants.COLS)
    height = len(constants.ROWS)
    
    # Crear un tablero visual (lista de listas)
    # El tamaño real es (height+1) x (width+1) para dejar espacio a las etiquetas de fila/columna
    display_board = [[" " for _ in range(width + 1)] for _ in range(height + 1)]
    
    # Agregar encabezados de columna (números 1, 2, 3...)
    for i, col_label in enumerate(constants.COLS, start=1):
        display_board[0][i] = col_label
    
    # Agregar encabezados de fila (letras A, B, C...)
    for i, row_label in enumerate(constants.ROWS, start=1):
        display_board[i][0] = row_label
        
    # Copiar contenido del tablero real al tablero visual
    for r in range(height):
        for c in range(width):
            val = board[r][c]
            if hide_ships and val == "S":
                val = " "
            display_board[r + 1][c + 1] = val
            
    # Imprimir el tablero completo con alineación de ancho fijo
    for row in display_board:
        print(" ".join(f"{cell:<3}" for cell in row))



