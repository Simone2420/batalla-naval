class Utils:
    pass

def get_column_letter(n: int) -> str:
    """
    Convierte un número entero (1-basado) en su letra de columna correspondiente.
    Ejemplo: 1 -> A, 26 -> Z, 27 -> AA, 28 -> AB, etc.
    """
    result = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        result = chr(65 + remainder) + result
    return result

def get_coords(ROWS,row: str, col: str) -> tuple[int, int]:
    """
    Convierte coordenadas textuales (ej: "B2") a índices numéricos (fila, columna).
    """
    # 1. Obtener fila: Convertir letra -> índice basado en 1, luego ajustar a 0-basado
    row_index = ROWS.index(row.upper()) + 1
    
    # 2. Obtener columna: Convertir String -> Entero, luego ajustar a 0-basado
    col_index = int(col) # int("1") es 1, int("26") es 26
    
    # Ajuste: El tablero está indexado desde (0,0) en código, pero las coordenadas de usuario empiezan en (1,1)
    # Por lo tanto, restamos 1 a ambos para que "A1" mapee a (0,0)
    return row_index - 1, col_index - 1

def get_text_coords(ROWS,COLS,row_idx: int, col_idx: int) -> tuple[str, str]:
    """
    Convierte coordenadas numéricas (índices) a coordenadas textuales (ej: ("A", "1")).
    """
    # Obtener letra de la fila
    # Sumamos 1 al índice porque ROWS está basado en 1 (A=1, B=2...)
    row_letter = ROWS[row_idx]
    
    # Obtener número de columna
    # Sumamos 1 al índice porque COLS está basado en 1 (1=1, 2=2...)
    col_number = COLS[col_idx]
    
    return row_letter, col_number

def parse_coordinate(input_str: str) -> tuple[str, str] | tuple[None, None]:
    """
    Parsea una coordenada ingresada (ej: "B2", "AA 15") y separa la parte de letras de los números.
    Retorna (letras, números) o (None, None) si no es válida.
    """
    input_str = input_str.strip().upper()
    if not input_str:
        return None, None
        
    letters = ""
    numbers = ""
    for char in input_str:
        if char.isalpha():
            letters += char
        elif char.isdigit():
            numbers += char
            
    if not letters or not numbers:
        return None, None
        
    return letters, numbers
