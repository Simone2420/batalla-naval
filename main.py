import os
import constants
from core import *
from utils import *

def clear_screen():
    # Limpia la pantalla en Windows ('cls') o Unix/macOS ('clear')
    os.system('cls' if os.name == 'nt' else 'clear')

class Game:
    def __init__(self):
        self.player_1 = Player("Jugador 1")
        self.player_2 = Player("Jugador 2")
        self.turn = Turn(self.player_1)
        self.is_game_over = False

    def setup_game(self):
        self.player_1.board.place_ships_randomly()
        self.player_2.board.place_ships_randomly()

    def game_loop(self):
        clear_screen()
        print("=========================================")
        print("       BIENVENIDO A BATALLA NAVAL        ")
        print("=========================================\n")
        print("Colocando los barcos del Jugador 1 de forma aleatoria...")
        print("Colocando los barcos del Jugador 2 de forma aleatoria...")
        input("\n¡Todos los barcos han sido colocados! Presiona Enter para comenzar la batalla...")

        while not self.is_game_over:
            clear_screen()

            # Determinar quién es el jugador activo y su oponente
            if self.turn.player == self.player_1:
                active_name = self.player_1.name
                own_board = self.player_1.board
                opponent_board = self.player_2.board
            else:
                active_name = self.player_2.name
                own_board = self.player_2.board
                opponent_board = self.player_1.board

            print("=========================================")
            print(f"         TURNO DE: {active_name}         ")
            print("=========================================\n")

            # Mostrar Radar (tablero del oponente ocultando barcos)
            print("RADAR (Tus disparos en el campo enemigo):")
            opponent_board.print_board(hide_ships=True)
            print("\n" + "-" * 50 + "\n")

            # Mostrar Tablero Propio (tus barcos y disparos del enemigo)
            print("TU TABLERO (Tus barcos y ataques enemigos):")
            own_board.print_board(hide_ships=False)
            print("\n")

            # Bucle de disparo del jugador activo (repite si acierta)
            turn_active = True
            while turn_active:
                coord_input = input(f"{active_name}, ingresa la coordenada de tu disparo (ej: B2): ")

                # Parsear coordenada
                row_letter, col_str = parse_coordinate(coord_input)
                if not row_letter or not col_str:
                    print("Error: Coordenada inválida. Debe tener formato de letra y número (ej: B2).")
                    continue

                # Verificar si la fila está en ROWS
                if row_letter not in constants.ROWS:
                    print(f"Error: La fila '{row_letter}' no existe en el tablero.")
                    continue

                # Verificar si la columna está en COLS
                if col_str not in constants.COLS:
                    print(f"Error: La columna '{col_str}' no existe en el tablero.")
                    continue

                # Convertir a índices
                row_idx, col_idx = get_coords(constants.ROWS, row_letter, col_str)

                # Procesar el disparo en el tablero del oponente
                valid_shot, message = opponent_board.handle_shot(row_idx, col_idx)
                if not valid_shot:
                    print(f"Error: {message}")
                    continue  # Pide la coordenada de nuevo sin gastar el turno

                print(f"\nResultado del disparo: {message}")

                # Verificar fin del juego tras cada disparo
                if not opponent_board.has_ships_remaining():
                    print(f"\n¡FELICIDADES {active_name}! Has hundido todos los barcos enemigos.")
                    print("¡Has ganado la partida!")
                    self.is_game_over = True
                    break

                # Si acierta, sigue disparando en su mismo turno
                if message == "¡TOCADO!":
                    print("\n=========================================")
                    print("¡SIGUE DISPARANDO! (Repites turno por acertar)")
                    print("=========================================\n")

                    # Mostrar tableros actualizados para que decida su próximo tiro
                    print("RADAR (Tus disparos en el campo enemigo):")
                    opponent_board.print_board(hide_ships=True)
                    print("\n" + "-" * 50 + "\n")

                    print("TU TABLERO (Tus barcos y ataques enemigos):")
                    own_board.print_board(hide_ships=False)
                    print("\n")
                else:
                    # Si falla (Agua...), termina su turno
                    turn_active = False

            if self.is_game_over:
                break

            # Esperar confirmación antes de pasar el turno y limpiar pantalla
            input("\nPresiona Enter para terminar tu turno y ocultar tus tableros...")
            self.turn.switch_turn(self.player_1, self.player_2)

        print("\n¡Gracias por jugar a la Batalla Naval!")

def main():
    game = Game()
    game.setup_game()
    game.game_loop()

if __name__ == "__main__":
    main()



