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
    print(end='        ')
    for col in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
        print(col, end='    ')
    print()
    print('     +----+----+----+----+----+----+----+----+     ')
    for row in range(7, -1, -1):
        print('  ' + str(row + 1), end='  ')
        for col in range(8):
            print('| ' + board.cell(row, col), end=' ')
        print('| ' + str(row + 1))
        print('     +----+----+----+----+----+----+----+----+     ')
    print(end='        ')
    for col in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
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
        print('    exit                        -- выход')
        print('    <row;col> <row1;col1>       -- ход из клетки (row, col)')
        print('                                   в клетку (row1, col1);')
        print('                                   например, e2 e4')

        # Выводим приглашение игроку нужного цвета
        if board.current_player_color() == WHITE:
            print('Ход белых:')
        else:
            print('Ход черных:')
        command = input()

        if command == 'exit':
            break
        if command == '':
            continue
        row, col, row1, col1 = translate(command)

        if board.move_piece(row, col, row1, col1):
            print('Ход успешен')
            print('-' * 50)
        else:
            print('Координаты некорректы! Попробуйте другой ход!')


def translate(coordinats):
    a, b = coordinats.split()
    return int(a[1]) - 1, 'abcdefgh'.index(a[0]), int(b[1]) - 1, 'abcdefgh'.index(b[0])


class Chessman:
    """Класс, являющийся базой для всех шахматных фигур"""

    def __init__(self, color):
        self.color = color

    def char(self):
        """возвращает имя фигуры"""
        return 'None'

    def get_color(self):
        """возвращает цвет фигуры"""
        return self.color

    def can_move(self, row, col, row1, col1, field, flag):
        """может ли выбранная фигура походить на данную клетку"""
        return False

    def can_attack(self, row, col, row1, col1, field, flag):
        """может ли выбранная фигура съесть фигуру на данной клетке"""
        return self.can_move(row, col, row1, col1, field, flag)


class Board:
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
        for j in range(8): # все пешки
            self.field[1][j] = Pawn(WHITE)
            self.field[6][j] = Pawn(BLACK)
        for i in range(2): # остальные фигуры
            # при i = 0 сначала выставляются фигуры на левой половине доски,
            # при i = 1 на правой
            self.field[0][7 * i] = Rook(WHITE) 
            self.field[7][7 * i] = Rook(BLACK)
            self.field[0][1 + 5 * i] = Knight(WHITE) 
            self.field[7][1 + 5 * i] = Knight(BLACK)
            self.field[0][2 + 3 * i] = Bishop(WHITE) 
            self.field[7][2 + 3 * i] = Bishop(BLACK)
        self.field[7][3] = Queen(BLACK)
        self.field[0][3] = Queen(WHITE)
        self.field[7][4] = King(BLACK)
        self.field[0][4] = King(WHITE)

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

        if self.is_move_avaliable(row, col, row1, col1):
            if (isinstance(self.field[row1][col1], Pawn) 
                    and abs(row - row1) == 2): # если пешка походила на две клетки, то её можно взять на проходе
                self.is_can_be_taken_on_pass = (int((row + row1) / 2), col, row1, col1) # запоминаем координаты клетки, через которую она прошла,
                                                                                        # и координаты самой пешки
            else:
                self.is_can_be_taken_on_pass = None  # удаляем информацию о пешки, т.к. наступил следующий ход

            self.color = opponent(self.color)  # передаём ход другому игроку
            return True
        return False

    def is_move_avaliable(self, row, col, row1, col1):
        """Проверка возможен ли данный ход"""

        if not correct_coords(row, col) or not correct_coords(row1, col1): 
            return False  # одна из клеток неверно введена

        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку

        piece = self.field[row][col]

        if piece is None:
            return False  # начальная клетка пустая

        if piece.get_color() != self.color:
            return False  # нельзя ходить не своими фигурами

        if self.field[row1][col1] is None:
            flag = piece.can_move(row, col, row1, col1, self.field, self.is_can_be_taken_on_pass)
            if flag[0] is False:
                return False
            self.field = flag[1]
            return True
        flag = piece.can_attack(row, col, row1, col1, self.field, self.is_can_be_taken_on_pass)
        if flag[0] is False:
            return False
        self.field = flag[1]
        return True


class Rook(Chessman):
    """Фигура ладья"""

    def __init__(self, color):
        self.color = color
        self.flag = False

    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'R'

    def can_move(self, row, col, row1, col1, field, flag):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""

        if row1 != row and col != col1:
            return False, None  # можно ходить только по горизонтали или только по вертикали
        if row1 == row and col == col1:
            return False, None  # нельзя ходить на ту же клетку
        if not self.is_way_clear(row, col, row1, col1, field):
            return False, None
        new_field = field
        new_field[row1][col1] = new_field[row][col]
        new_field[row][col] = None
        self.flag = True
        return True, new_field

    def is_way_clear(self, row, col, row1, col1, field):
        """Проверка, есть ли другие фигуры на пути.
        Фигура на назначенной клетки -- исключение, если она другого цвета"""

        if row1 == row:
            d = int((col - col1) / abs(col - col1))
            for i in range(1, abs(col - col1)):
                if field[row1][col - i * d] is not None:
                    return False

        if col1 == col:
            d = int((row - row1) / abs(row1 - row))
            for i in range(1, abs(row - row1)):
                if field[row - i * d][col1] is not None:
                    print(7)
                    return False

        if field[row1][col1] is not None:
            if field[row1][col1].get_color() == self.get_color():
                return False
        return True

    def get_flag(self):
        """ходила ли данная фигура"""
        return self.flag


class Bishop(Chessman):
    """Фигура слон"""

    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'B'
    
    def can_move(self, row, col, row1, col1, field, flag):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""

        if abs(row1 - row) != abs(col - col1):
            return False, None  # можно ходить только по диагонали
        if row1 == row and col == col1:
            return False, None  # нельзя ходить на ту же клетку
        if not self.is_way_clear(row, col, row1, col1, field):
            return False, None
        new_field = field
        new_field[row1][col1] = new_field[row][col]
        new_field[row][col] = None
        return True, new_field

    def is_way_clear(self, row, col, row1, col1, field):
        """Проверка, есть ли другие фигуры на пути.
        Фигура на назначенной клетки -- исключение, если она другого цвета"""
        
        d_row = int((row - row1) / abs(row - row1))
        d_col = int((col - col1) / abs(col - col1))
        for i in range(1, abs(row - row1)):
            if field[row - i * d_row][col - i * d_col] is not None:
                return False

        if field[row1][col1] is not None:
            if field[row1][col1].get_color() == self.get_color():
                return False
        return True


class Knight(Chessman):
    """Фигура конь"""
    
    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'N'
    
    def can_move(self, row, col, row1, col1, field, flag):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""

        if not self.is_way_clear(row1, col1, field):
            return False, None
        if abs(row1 - row) == 2 and abs(col - col1) == 1:
            new_field = field
            new_field[row1][col1] = new_field[row][col]
            new_field[row][col] = None
            return True, new_field  # можно ходить только буквой Г
        if abs(row1 - row) == 1 and abs(col - col1) == 2:
            new_field = field
            new_field[row1][col1] = new_field[row][col]
            new_field[row][col] = None
            return True , new_field
        return False, None

    def is_way_clear(self, row, col, field):
        """Проверка, есть ли другие фигуры на пути.
        Фигура на назначенной клетки -- исключение, если она другого цвета"""

        if field[row][col] is not None:
            if field[row][col].get_color() == self.get_color():
                return False
        return True


class Queen(Chessman):
    """Фигура ферзь"""

    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'Q'
    
    def can_move(self, row, col, row1, col1, field, flag):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""

        if row1 != row and col != col1 and abs(row1 - row) != abs(col - col1):
            return False, None  # можно ходить только по горизонтали, или только по вертикали, или только по диагонали
        if row1 == row and col == col1:
            return False, None  # нельзя ходить на ту же клетку
        if not self.is_way_clear(row, col, row1, col1, field):
            return False, None
        new_field = field
        new_field[row1][col1] = new_field[row][col]
        new_field[row][col] = None
        return True, new_field

    def is_way_clear(self, row, col, row1, col1, field):
        """Проверка, есть ли другие фигуры на пути.
        Фигура на назначенной клетки -- исключение, если она другого цвета"""

        
        if row1 == row:
            d = int((col - col1) / abs(col - col1))
            for i in range(1, abs(col - col1)):
                if field[row1][col - i * d] is not None:
                    return False

        if col1 == col:
            d = int((row - row1) / abs(row - row1))
            for i in range(1, abs(row - row1)):
                if field[row - i * d][col1] is not None:
                    return False

        if abs(row1 - row) == abs(col1 - col):
            d_row = int((row - row1) / abs(row - row1))
            d_col = int((col - col1) / abs(col - col1))
            for i in range(1, abs(row - row1)):
                if field[row - i * d_row][col - i * d_col] is not None:
                    return False

        if field[row1][col1] is not None:
            if field[row1][col1].get_color() == self.get_color():
                return False
        return True


class Pawn(Chessman):
    """Фигура пешка"""

    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'P'

    def can_move(self, row, col, row1, col1, field, flag):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку.
        Возвращается (False, False) если ход невозможен
        (True, False) -- при обычном ходе вперёд или при взятии другой фигуры
        (True, True) -- при взятии на проходе"""

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
            end_row = 7
        else:
            direction = -1
            start_row = 6
            end_row = 0

        if col1 == col:  # обычный или длинный ход
            # ход на 1 клетку
            if row + direction == row1:
                if field[row1][col1] is None:
                    new_field = field
                    new_field[row1][col1] = new_field[row][col]
                    new_field[row][col] = None
                    if row1 == end_row:
                        flag2 = self.upgrade_pawn(row1, col1, new_field)
                        if flag2[0]:
                            new_field = flag2[1]
                    return True, new_field
 
            # ход на 2 клетки из начального положения
            if row == start_row and row + 2 * direction == row1:
                if (field[row1][col1], field[int((row + row1) / 2)][col1]) == (None, None):
                    new_field = field
                    new_field[row1][col1] = new_field[row][col]
                    new_field[row][col] = None
                    return True, new_field

        if row1 - row == direction and abs(col1 - col) == 1:
            if field[row1][col1] is not None:
                if self.get_color() == field[row1][col1].get_color():
                    return False, None
                new_field = field
                new_field[row1][col1] = new_field[row][col]
                new_field[row][col] = None
                if row1 == end_row:
                    flag2 = self.upgrade_pawn(row1, col1, new_field)
                    if flag2[0]:
                        new_field = flag2[1]
                return True, new_field
            if flag is not None:
                if (flag[0], flag[1]) == (row1, col1):
                    new_field = field
                    new_field[row1][col1] = new_field[row][col]
                    new_field[row][col] = None
                    new_field[row][col1] = None
                    return True, new_field
        return False, None

    def can_attack(self, row, col, row1, col1, field, flag):
        """Функция, проверяющая, бьёт ли эта пешка эту клетку"""

        if self.color == WHITE:
            direction = 1
            end_row = 7
        else:
            direction = -1
            end_row = 0

        if row1 - row == direction and abs(col1 - col) == 1:
            new_field = field
            new_field[row1][col1] = new_field[row][col]
            new_field[row][col] = None
            if row1 == end_row:
                flag2 = self.upgrade_pawn(row1, col1, new_field)
                if flag2[0]:
                    new_field = flag2[1]
            return True, new_field

        return False, None

    def upgrade_pawn(self, row, col, field):
        """замена пешки на другую фигуру при достижении противоложного края доски"""
        char = input("Введите на какую фигуру заменить пешку (N, R, Q, B): ")
        if char not in ['N', 'R', 'Q', 'B']:
            return False, None
        if char == 'N':
            new_field = field
            new_field[row][col] = Knight(self.color)
        if char == 'R':
            new_field = field
            new_field[row][col] = Rook(self.color)
        if char == 'Q':
            new_field = field
            new_field[row][col] = Queen(self.color)
        if char == 'B':
            new_field = field
            new_field[row][col] = Bishop(self.color)
        return True, new_field


class King(Chessman):
    """Фигура король"""

    def __init__(self, color):
        self.flag = False
        self.color = color

    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'K'
    
    def can_move(self, row, col, row1, col1, field, flag):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""
        
        new_field = field
        if row1 == row and col == col1:
            return False  # нельзя ходить на ту же клетку
        if (abs(row - row1) <= 1 and abs(col - col1) <= 1 
            and self.is_way_clear(row1, col1, field) 
            and not self.is_under_attack(row1, col1, field, flag, row, col, col)):
            self.flag = False
            new_field[row1][col1] = new_field[row][col]
            new_field[row][col] = None
            return True, new_field
        if col1 - col == 2 and field[row][7] is not None:
            if (not (field[row][7].get_flag() and self.flag) and
                    (field[row][6], field[row][5]) == (None, None) and not
                    self.is_under_attack(row, 5, field, flag, row, 7, 4) and not
                    self.is_under_attack(row, 6, field, flag, row, 7, 4)):
                new_field[row][5] = new_field[row][7]
                new_field[row][7] = None
                new_field[row][6] = new_field[row][4]
                new_field[row][4] = None
                self.flag = True
                return True, new_field
            return False, None
        if col - col1 == 2 and field[row][0] is not None:
            if (not (field[row][0].get_flag() and self.flag) and
                    (field[row][1], field[row][2], field[row][3]) == (None, None, None)
                    and not self.is_under_attack(row, 2, field, flag, row, 0, 4) and not
                    self.is_under_attack(row, 3, field, flag, row, 0, 4)):
                new_field[row][3] = new_field[row][0]
                new_field[row][0] = None
                new_field[row][2] = new_field[row][4]
                new_field[row][4] = None
                self.flag = True
                return True, new_field
        
        return False, None

    def is_under_attack(self, row, col, field, flag, row1, col1, col2):
        p1, p2 = field[row1][col2], field[row1][col1]
        field[row1][col2] = None
        field[row1][col1] = None
        for i in range(8):
            for j in range(8):
                if field[i][j] is None:
                    continue
                if (field[i][j].get_color() != self.color 
                        and field[i][j].can_attack(i, j, row, col, field, flag)[0]):
                    field[row1][col2], field[row1][col1] = p1, p2
                    return True
        field[row1][col2], field[row1][col1] = p1, p2
        return False

    def is_way_clear(self, row, col, field):
        """Проверка, есть ли другие фигуры на пути.
        Фигура на назначенной клетки -- исключение, если она другого цвета"""

        if field[row][col] is not None:
            if field[row][col].get_color() == self.get_color():
                return False
        return True

    
if __name__ == "__main__":
    main()
