def correct_coords(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row < 8 and 0 <= col < 8


class Chessman:
    """Класс, являющийся базой для всех шахматных фигур"""
    def __init__(self, row, col, color):
        self.set_position(row, col)
        self.color = color
        self.name = self.char(self)

    def char(self):
        """Функция, возвращающая имя фигуры"""
        return None

    def get_color(self):
        """Функция, возвращающая цвет фигуры"""
        return self.color

    def set_position(self, row, col):
        """Функция, устанавливающая фигуру на заданную позицию"""
        self.row = row
        self.col = col


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        # Пешка белого цвета в клетке E2.
        self.field[1][4] = Pawn(1, 4, WHITE)  

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        """Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела."""
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def move_piece(self, row, col, row1, col1):
        """Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернет True.
        Если нет --- вернет False"""

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if not piece.can_move(row1, col1):
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        piece.set_position(row1, col1)
        self.color = opponent(self.color)
        return True


class Pawn(Chessman):
    """Фигура пешка"""

    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'P'

    def can_move(self, row, col):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""

        # Пешка может ходить только по вертикали
        # Взятие на ходу не реализовано !!!
        if self.col != col:
            return False

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6
 
        # ход на 1 клетку
        if self.row + direction == row:
            return True
 
        # ход на 2 клетки из начального положения
        if self.row == start_row and self.row + 2 * direction == row:
            return True
 
        return False


class Rook(Chessman):
    """Фигура ладья"""

    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'R'

    def can_move(self, row, col):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""

        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if self.row != row and self.col != col:
            return False
 
        return True


class Queen(Chessman):
    """Фигура ферзь"""

    def can_move(self, row, col):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""

        # Ферзь может ходить либо по диогонали, либо по вертикали
        # либо по горизонтали. 
        if ((abs(self.row - row) == abs(self.col - col)
                 or self.row == row or self.col == col)):
            return True
        return False
    
    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'Q'


class Bishop(Chessman):
    """Фигура слон"""
        
    def can_move(self, row, col):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""

        # Слон может ходить только по диагоналям
        if abs(self.row - row) == abs(self.col - col):
            return True
        return False
    
    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'B'


class Knight(Chessman):
    """Фигура конь"""
        
    def can_move(self, row, col):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""

        # Конь ходит буквой 'Г', то есть в любую сторону на 2 клетки и одну в бок
        if ((abs(self.row - row) == 1 and abs(self.col - col) == 2) or
                 (abs(self.row - row) == 2 and abs(self.col - col) == 1)):
            return True
        return False
    
    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'N'
