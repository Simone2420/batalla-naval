import random
import constants
from utils import get_coords

class Player:
    def __init__(self,name: str):
        self.name = name
        self.board = Board(constants.GRID_HEIGHT, constants.GRID_WIDTH)

class Turn:
    def __init__(self,player: Player):
        self.player = player
        self.status = True
        self.turn_number = 1
    def next_turn(self):
        self.status = True
        self.turn_number += 1
    def switch_turn(self,player1: Player, player2: Player):
        if self.player == player1:
            self.player = player2
        else:
            self.player = player1
        self.next_turn()

            

class Board:
    def __init__(self,height: int, width: int):
        self.height = height
        self.width = width
        self.board = self.initialize_board()

    
    def initialize_board(self):
        board = [[" " for _ in range(self.width)] for _ in range(self.height)]
        return board
    
    def can_place_ship(self, row, col, size, orientation):
        orientation = orientation.upper()
    
        if orientation == 'H':
            if col + size > self.width:
                return False
            for c in range(col, col + size):
                if self.board[row][c] != " ":
                    return False
        elif orientation == 'V':
            if row + size > self.height:
                return False
            for r in range(row, row + size):
                if self.board[r][col] != " ":
                    return False
        else:
            return False
        
        return True

    def place_ship(self, row, col, size, orientation):
        orientation = orientation.upper()
        if orientation == 'H':
            for c in range(col, col + size):
                self.board[row][c] = "S"
        elif orientation == 'V':
            for r in range(row, row + size):
                self.board[r][col] = "S"

    def place_ships_randomly(self):
        
        for ship_name, size in constants.SHIP_SIZES.items():
            placed = False
            attempts = 0
            while not placed and attempts < 1000:
                orientation = random.choice(['H', 'V'])
                row = random.randint(0, self.height - 1)
                col = random.randint(0, self.width - 1)
                
                if self.can_place_ship(row, col, size, orientation):
                    self.place_ship(row, col, size, orientation)
                    placed = True
                attempts += 1
        if not placed:
            raise RuntimeError(f"No se pudo colocar el barco '{ship_name}' de tamaño {size} después de 1000 intentos.")


    def handle_shot(self, row, col):
        """
        Procesa un disparo en el tablero del oponente.
        Retorna una tupla (validez_disparo, mensaje).
        """
    
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            return False, "Coordenadas fuera del tablero."
        
        cell = self.board[row][col]
        if cell == "X" or cell == "-":
            return False, "Ya has disparado en esta coordenada anteriormente."
        
        if cell == "S":
            self.board[row][col] = "X"
            return True, "¡TOCADO!"
        else:
            self.board[row][col] = "-"
            return True, "Agua..."

    def has_ships_remaining(self):
        """
        Devuelve True si aún queda algún barco ("S") intacto en el tablero.
        """
        for row in self.board:
            if "S" in row:
                return True
        return False

    def print_board(self, hide_ships=False):
        """
        Genera y muestra el tablero visual con etiquetas de filas (letras) y columnas (números).
        Si hide_ships es True, oculta los barcos ("S") reemplazándolos con espacios vacíos.
        """
    
        # Crear un tablero visual (lista de listas)
        # El tamaño real es (height+1) x (width+1) para dejar espacio a las etiquetas de fila/columna
        display_board = [[" " for _ in range(self.width + 1)] for _ in range(self.height + 1)]
    
        # Agregar encabezados de columna (números 1, 2, 3...)
        for i, col_label in enumerate(constants.COLS, start=1):
            display_board[0][i] = col_label
    
        # Agregar encabezados de fila (letras A, B, C...)
        for i, row_label in enumerate(constants.ROWS, start=1):
            display_board[i][0] = row_label
        
        # Copiar contenido del tablero real al tablero visual
        for r in range(self.height):
            for c in range(self.width):
                val = self.board[r][c]
                if hide_ships and val == "S":
                    val = " "
                display_board[r + 1][c + 1] = val
            
        # Imprimir el tablero completo con alineación de ancho fijo
        for row in display_board:
            print(" ".join(f"{cell:<3}" for cell in row))



