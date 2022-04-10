WHITE = 1
BLACK = 2


def correct_coords(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row < 8 and 0 <= col < 8



def opponent(color): # Удобная функция для вычисления цвета противника
    if color == WHITE:
        return BLACK
    return WHITE


def print_board(board): # Распечатать доску в текстовом виде
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()
 

def main():
    # Создаём шахматную доску
    board = Board()

    # Цикл ввода команд игроков
    while True:

        # Выводим положение фигур на доске
        print_board(board)

        # Подсказка по командам
        print('Команды:')
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <col1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')

        # Выводим приглашение игроку нужного цвета
        if board.current_player_color() == WHITE:
            print('Ход белых:')
        else:
            print('Ход черных:')
        command = 'move ' + input()

        if command == 'exit':
            break
        if command == 'move ':
            continue
        move_type, row, col, row1, col1 = command.split()
        row, col, row1, col1 = int(row), int(col), int(row1), int(col1)

        if board.move_piece(row, col, row1, col1):
            print('Ход успешен')
        else:
            print('Координаты некорректы! Попробуйте другой ход!')


class Chessman:
    """Класс, являющийся базой для всех шахматных фигур"""

    def __init__(self, row, col, color):
        self.set_position(row, col)
        self.color = color
        self.name = self.char()

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
    """Поле с фигурами"""

    def __init__(self):
        self.color = WHITE # цвет фигур, игрока который сейчас ходит

        self.is_can_be_taken_on_pass = None # координаты пешки, которую могут 
                                            # взять на проходе после данного хода;
                                            # записывается скачала координаты клетки,
                                            # через которую она ходила, потом координаты самой пешки
        # создаём поле с фигурами
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)

        # расставляем все фигуры

        """   
        for j in range(8): # все пешки
            self.field[1][j] = Pawn(1, j, WHITE)
            self.field[6][j] = Pawn(6, j, BLACK)
        for i in range(2): # остальные фигуры
            # при i = 0 сначала выставляются фигуры на левой половине доски,
            # при i = 1 на правой
            self.field[0][7 * i] = Rook(0, 7 * i, WHITE) 
            self.field[7][7 * i] = Rook(7, 7 * i, BLACK)
            self.field[0][1 + 5 * i] = Knight(0, 1 + 5 * i, WHITE) 
            self.field[7][1 + 5 * i] = Knight(7, 1 + 5 * i, BLACK)
            self.field[0][2 + 3 * i] = Bishop(0, 2 + 3 * i, WHITE) 
            self.field[7][2 + 3 * i] = Bishop(7, 2 + 3 * i, BLACK)
        """

        #self.field[7][3] = Queen(7, 3, BLACK)
        #self.field[0][3] = Queen(0, 3, WHITE)
        self.field[2][4] = King(2, 4, BLACK)
        self.field[0][4] = King(0, 4, WHITE)

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

    def remove_chessman(self, row, col):
        self.field[row][col] = None

    def move_piece(self, row, col, row1, col1):
        """Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернет True.
        Если нет --- вернет False"""

        if not correct_coords(row, col) or not correct_coords(row1, col1): 
            return False  # одна из клеток неверно введена

        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку

        piece = self.field[row][col]

        if piece is None:
            print('|||||| начальная клетка пустая')
            return False  # начальная клетка пустая

        if piece.get_color() != self.color:
            print('|||||| нельзя ходить не своими фигурами')
            return False  # нельзя ходить не своими фигурами

        if not isinstance(piece, Pawn):
            if not piece.can_move(row1, col1):
                print('||||||| выбранная фигура не может походить в выбранную клетку')
                return False  # выбранная фигура не может походить в выбранную клетку

        if isinstance(piece, Pawn):  # у пешки возможны чуть более сложные ходы,
                                     # поэтому её следует рассматривать отдельно
            flag = piece.can_move(row1, col1, self.is_can_be_taken_on_pass, self.field)
            if not flag[0]:  # ход не возможен по любой из причин
                return False
            if flag[1]:
                # пешка ловит на проходе,
                # поэтому следует убрать пойманную пешку с доски
                self.remove_chessman(self.is_can_be_taken_on_pass[2], self.is_can_be_taken_on_pass[3])
                # иначе просто ходит или ест другую фигуру,
                # никаких дополнительных действий не нужно

        if not piece.is_way_clear(row1, col1, self.field):
            print('||||||| нельзя проходить через другие фигуры')
            return False  # нельзя проходить через другие фигуры (исключение -- конь)

        if isinstance(piece, King) and self.is_under_attack(row, col, opponent(self.current_player_color())):
            print('||||||| нельзя ходить королём на клетки, которые бьются другими фигурами')
            return False  # нельзя ходить королём на клетки, которые бьются другими фигурами

        # если программа дошла до этого момента,
        # значит такой ход возможен

        self.remove_chessman(row, col)  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.

        if isinstance(piece, Pawn) and abs(row - row1) == 2: # если пешка походила на две клетки, то её можно взять на проходе
            self.is_can_be_taken_on_pass = (int((row + row1) / 2), col, row1, col1) # запоминаем координаты клетки, через которую она прошла,
                                                                                    # и координаты самой пешки
        else:
            self.is_can_be_taken_on_pass = None  # если пешку не взяли на проходе, удаляем информацию о ней

        piece.set_position(row1, col1)  # обновляем информацию о фигуре
        self.color = opponent(self.color)  # передаём ход другому игроку
        return True

    def is_under_attack(self, row, col, color):
        """Проверка, находится ли данная клетка под атакой других фигур данного цвета"""
        for i in range(8):
            for j in range(8):
                if self.field[i][j] is not None: # у каждой фигуры данного цвета (которая ещё находится на поле) 
                                                 # бьёт ли она эту клетку
                    if color == self.field[i][j].get_color():
                        if isinstance(self.field[i][j], Pawn):  # у пешки немного отличающаяся система хода, проверяем её отдельно от других фигур
                            if self.field[i][j].can_move(row, col, self.is_can_be_taken_on_pass, self.field):
                                return True
                        if self.field[i][j].can_move(row, col):
                            print(self.field[i][j].char(), self.field[i][j].row , self.field[i][j].col)
                            return True
                        
        return False


class Pawn(Chessman):
    """Фигура пешка"""

    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'P'

    def can_move(self, row, col, is_can_be_taken_on_pass, field):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""

        if abs(self.col - col) == 1 and abs(self.row - row) == 1:  
            # ходит по диагонали только когда ест другую фигуру
            piece = field[row][col]
            if piece is not None:
                if piece.get_color() != self.get_color():
                    return True, False  # так ходить можно, дополнительно другие фигуры удалять не нужно
            else:
                if is_can_be_taken_on_pass is not None:
                    if (row, col) == (is_can_be_taken_on_pass[0], is_can_be_taken_on_pass[1]):
                        return True, True  # пешка может съесть другую на проходе,
                                           # нужно убрать вторую с доски

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6
 
        # ход на 1 клетку
        if self.row + direction == row and self.col == col:
            return True, False
 
        # ход на 2 клетки из начального положения
        if self.row == start_row and self.row + 2 * direction == row:
            return True, False
 
        return False, False

    def is_way_clear(self, row, col, field):
        """Проверка на то, есть ли на пути другие фигуры.
        Если их нет или на назначенной клетке стоит фигура другого цвета
        возвращается True"""

        if field[row][col] is not None and self.col - col != 0:
            print(21)
            return True
        if field[row][col] is not None:
            print(22)
            return False  # пешка не умеет есть по прямой
        if abs(self.row - row) == 1:
            print(24)
            return True
        else:
            print(23)
            if field[row + int((self.row - row) / abs(self.row - row))][col] is not None:
                return False # если пешка сделал длинный ход, то также нужно проверить промежуточную клетку
        return True


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

    def is_way_clear(self, row, col, field):
        """Проверка на то, есть ли на пути другие фигуры.
        Если их нет или на назначенной клетке стоит фигура другого цвета
        возвращается True"""
        if self.row == row: # движение по горизонтали
            for i in range(col, self.col, int((self.col - col) / abs(self.col - col))): 
                # перебираем все клетки от данной
                # до клетки где сейчас стоит фигура
                piece = field[self.row][i]
                if i == col:
                    if piece is not None:
                        if piece.get_color() == self.get_color():
                            return False
                    continue
                if piece is not None:
                    return False

        elif self.col == col: # движение по вертикали
            for i in range(row, self.row, int((self.row - row) / abs(self.row - row))): 
                # перебираем все клетки от данной
                # до клетки где сейчас стоит фигура
                piece = field[i][self.col]
                if i == row: 
                    # если на назначенной клетки стоит фигура другого цвета, 
                    # мы её игнорируем, т.е. мы её съедаем,
                    # иначе возвращаем False
                    if piece is not None:
                        if piece.get_color() == self.get_color():
                            return False
                    continue
                if piece is not None:
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

    def is_way_clear(self, row, col, field):
        """Проверка на то, есть ли на пути другие фигуры.
        Если их нет или на назначенной клетке стоит фигура другого цвета
        возвращается True"""
        if self.row == row: # движение по горизонтали
            for i in range(col, self.col, int((self.col - col) / abs(self.col - col))): 
                # перебираем все клетки от данной
                # до клетки где сейчас стоит фигура
                piece = field[self.row][i]
                if i == col: 
                    # если на назначенной клетки стоит фигура другого цвета, 
                    # мы её игнорируем, т.е. мы её съедаем,
                    # иначе возвращаем False
                    if piece is not None:
                        if piece.get_color() == self.get_color():
                            return False
                    continue
                if piece is not None:
                    return False

        elif self.col == col: # движение по вертикали
            for i in range(row, self.row, int((self.row - row) / abs(self.row - row))): 
                # перебираем все клетки от данной
                # до клетки где сейчас стоит фигура
                piece = field[i][self.col]
                if i == row:
                    if piece is not None:
                        if piece.get_color() == self.get_color():
                            return False
                    continue
                if piece is not None:
                    return False

        else: # движение по диагонали
            d1 = int((self.row - row) / abs(self.row - row)) # направление движения по горизонтали и по вертикали
            d2 = int((self.col - col) / abs(self.col - col))
            for i in range(abs(self.row - row)): 
                # перебираем все клетки от данной
                # до клетки где сейчас стоит фигура
                piece = field[row + i * d1][col + i * d2]
                if i == 0:
                    if piece is not None:
                        if piece.get_color() == self.get_color():
                            return False
                    continue
                if piece is not None:
                    return False

        return True


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

    def is_way_clear(self, row, col, field):
        """Проверка на то, есть ли на пути другие фигуры.
        Если их нет или на назначенной клетке стоит фигура другого цвета
        возвращается True"""
        d1 = int((self.row - row) / abs(self.row - row)) # направление движения по горизонтали и по вертикали
        d2 = int((self.col - col) / abs(self.col - col))
        for i in range(abs(self.row - row)): 
            # перебираем все клетки от данной
            # до клетки где сейчас стоит фигура
            piece = field[row + i * d1][col + i * d2]
            if i == 0:
                if piece is not None:
                    if piece.get_color() == self.get_color():
                        return False
                continue
            if piece is not None:
                return False

        return True


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

    def is_way_clear(self, row, col, field):
        piece = field[row][col]
        if piece is not None:
            if piece.get_color() == self.get_color():
                return False
        return True


class King(Chessman):
    """Фигура король"""

    def can_move(self, row, col):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""

        # Король может ходить либо по диогонали, либо по вертикали
        # либо по горизонтали на одну клетку.
        if (row, col) == (self.row, self.col):
            return False
        if abs(self.row - row) > 1 or abs(self.col - col) > 1:
            return False
        return True
    
    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'K'

    def is_way_clear(self, row, col, field):
        """Проверка на то, есть ли на пути другие фигуры.
        Если их нет или на назначенной клетке стоит фигура другого цвета
        возвращается True"""
        
        piece = field[row][col]
        if piece is not None:
            if piece.get_color() == self.get_color():
                return False
        
        return True

if __name__ == "__main__":
    main()

