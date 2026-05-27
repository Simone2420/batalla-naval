from utils import *

GRID_WIDTH = 10
GRID_HEIGHT = 10

ROWS = [get_column_letter(i) for i in range(1, GRID_HEIGHT + 1)]
COLS = [str(i) for i in range(1, GRID_WIDTH + 1)]

SHIP_SIZES = {
    "portaviones": 5,
    "acorazado": 4,
    "crucero": 3,
    "submarino": 3,
    "destructor": 2,
    #"tanque": 1
}
