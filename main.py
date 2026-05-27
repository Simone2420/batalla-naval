import os
import constants
import core
from utils import *

def clear_screen():
    # Limpia la pantalla en Windows ('cls') o Unix/macOS ('clear')
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print("=========================================")
    print("       BIENVENIDO A BATALLA NAVAL        ")
    print("=========================================\n")
    
    # 1. Inicializar tableros para los dos jugadores
    p1_board = core.initialize_board()
    p2_board = core.initialize_board()
    
    # 2. Fase de Colocación (Aleatoria)
    print("Colocando los barcos del Jugador 1 de forma aleatoria...")
    core.place_ships_randomly(p1_board)
    print("Colocando los barcos del Jugador 2 de forma aleatoria...")
    core.place_ships_randomly(p2_board)
    
    input("\n¡Todos los barcos han sido colocados! Presiona Enter para comenzar la batalla...")
    
    current_player = 1
    game_over = False
    
    # 3. Bucle de Turnos
    while not game_over:
        clear_screen()
        
        # Determinar quién es el jugador activo y su oponente
        if current_player == 1:
            active_name = "JUGADOR 1"
            own_board = p1_board
            opponent_board = p2_board
            next_player = 2
        else:
            active_name = "JUGADOR 2"
            own_board = p2_board
            opponent_board = p1_board
            next_player = 1
            
        print("=========================================")
        print(f"         TURNO DE: {active_name}         ")
        print("=========================================\n")
        
        # Mostrar Radar (tablero del oponente ocultando barcos)
        print("RADAR (Tus disparos en el campo enemigo):")
        core.print_board(opponent_board, hide_ships=True)
        print("\n" + "-" * 50 + "\n")
        
        # Mostrar Tablero Propio (tus barcos y disparos del enemigo)
        print("TU TABLERO (Tus barcos y ataques enemigos):")
        core.print_board(own_board, hide_ships=False)
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
            valid_shot, message = core.handle_shot(opponent_board, row_idx, col_idx)
            if not valid_shot:
                print(f"Error: {message}")
                continue  # Pide la coordenada de nuevo sin gastar el turno
                
            print(f"\nResultado del disparo: {message}")
            
            # Verificar fin del juego tras cada disparo
            if not core.has_ships_remaining(opponent_board):
                print(f"\n¡FELICIDADES {active_name}! Has hundido todos los barcos enemigos.")
                print("¡Has ganado la partida!")
                game_over = True
                break
                
            # Si acierta, sigue disparando en su mismo turno
            if message == "¡TOCADO!":
                print("\n=========================================")
                print("¡SIGUE DISPARANDO! (Repites turno por acertar)")
                print("=========================================\n")
                
                # Mostrar tableros actualizados para que decida su próximo tiro
                print("RADAR (Tus disparos en el campo enemigo):")
                core.print_board(opponent_board, hide_ships=True)
                print("\n" + "-" * 50 + "\n")
                
                print("TU TABLERO (Tus barcos y ataques enemigos):")
                core.print_board(own_board, hide_ships=False)
                print("\n")
            else:
                # Si falla (Agua...), termina su turno
                turn_active = False
                
        if game_over:
            break
            
        # Esperar confirmación antes de pasar el turno y limpiar pantalla
        input("\nPresiona Enter para terminar tu turno y ocultar tus tableros...")
        current_player = next_player

    print("\n¡Gracias por jugar a la Batalla Naval!")


if __name__ == "__main__":
    main()

