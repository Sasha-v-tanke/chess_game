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
        command = input()

        if command == 'exit':
            break
        if command == '':
            continue
        move_type, row, col, row1, col1 = command.split()
        row, col, row1, col1 = int(row), int(col), int(row1), int(col1)

        if board.move_piece(row, col, row1, col1):
            print('Ход успешен')
        else:
            print('Координаты некорректы! Попробуйте другой ход!')


class Chessman:
    """Класс, являющийся базой для всех шахматных фигур"""

    def __init__(self, color):
        self.color = color

    def get_color(self):
        """Функция, возвращающая цвет фигуры"""
        return self.color


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
        for j in range(8): # все пешки
            self.field[1][j] = Pawn(WHITE)
            self.field[6][j] = Pawn(BLACK)
        for i in range(2): # остальные фигуры
            # при i = 0 сначала выставляются фигуры на левой половине доски,
            # при i = 1 на правой
            self.field[0][7 * i] = Rook(WHITE) 
            self.field[7][7 * i] = Rook(BLACK)
            #self.field[0][1 + 5 * i] = Knight(WHITE) 
            #self.field[7][1 + 5 * i] = Knight(BLACK)
            #self.field[0][2 + 3 * i] = Bishop(WHITE) 
            #self.field[7][2 + 3 * i] = Bishop(BLACK)
        #self.field[7][3] = Queen(BLACK)
        #self.field[0][3] = Queen(WHITE)
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
            piece = self.field[row][col]
            self.field[row][col] = None  # Снять фигуру.
            self.field[row1][col1] = piece  # Поставить на новое место.

            if isinstance(piece, Pawn) and abs(row - row1) == 2: # если пешка походила на две клетки, то её можно взять на проходе
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
        
        if isinstance(piece, Pawn):  # у пешки возможны чуть более сложные ходы,
                                     # поэтому её следует рассматривать отдельно
            flag = piece.can_move(row1, col1, self.is_can_be_taken_on_pass, self)
            # flag = (bool, bool) 
            # первое - возможен ли ход
            # второе - было ли это взятием на проходе
            if not flag[0]:  # ход не возможен по любой из причин
                return False
            if flag[1]:
                # пешка ловит на проходе,
                # поэтому следует убрать пойманную пешку с доски
                self.field[self.is_can_be_taken_on_pass[2]][self.is_can_be_taken_on_pass[3]] = None
                # иначе пешка просто ходит или ест другую фигуру,
                # никаких дополнительных действий не нужно
            return True

        # если данный ход ставит своего же короля под удар, вернуть False.
        # если королю шах, и выбранная фигура не король, вернуть False. Не реализовано
        if isinstance(piece, King) and self.is_under_attack(row1, col1, opponent(self.current_player_color())):
            return False  # Нельзя ходить королём на клетки, которые бьются другими фигурами.
        if isinstance(piece, King):
            new_field = piece.can_move(row, col, row1, col1, self)
            if new_field is not False:
                self.field = new_field
                print(1)
                return True
            return False
        if not piece.can_move(row, col, row1, col1, self):
            print(2)
            return False  # выбранная фигура не может походить в выбранную клетку

        
        return True

    def is_under_attack(self, row1, col1, color):
        """Проверка, находится ли данная клетка под атакой других фигур данного цвета"""

        for i in range(8):
            for j in range(8):
                piece = self.field[i][j]
                if piece is not None:
                    if color == piece.get_color():
                        if isinstance(piece, Pawn):  # у пешки немного отличающаяся система хода, проверяем её отдельно от других фигур
                            if piece.can_eat(i, j, row1, col1, self.is_can_be_taken_on_pass, self):
                                print(4)
                                return True
                            continue
                        if piece.can_move(i, j, row1, col1, self):
                            print()
                            return True
        return False

    
class Pawn(Chessman):
    """Фигура пешка"""

    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'P'

    def can_move(self, row, col, row1, col1, flag, field):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку.
        Возвращается (False, False) если ход невозможен
        (True, False) -- при обычном ходе вперёд или при взятии другой фигуры
        (True, True) -- при взятии на проходе"""

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        if col1 == col:  # обычный или длинный ход
            # ход на 1 клетку
            if row + direction == row1:
                if field[row1][col1] is None:
                    return True, False
 
            # ход на 2 клетки из начального положения
            if row == start_row and row + 2 * direction == row1:
                if (field[row1][col1], field[int((row + row1) / 2)][col1]) == (None, None):
                    return True, False
        if row1 - row == direction and abs(col1 - col) == 1:
            if field[row1][col1] is not None:
                return self.get_color() != field[row1][col1].get_color(), False
            if flag is not None:
                if (flag[0], flag[1]) == (row1, col1):
                    return True, True
        return False, False

    def can_eat(self, row, col, row1, col1, flag, field):
        """Функция, проверяющая, бьёт ли эта пешка эту клетку"""

        if self.color == WHITE:
            direction = 1
        else:
            direction = -1

        if row1 - row == direction and abs(col1 - col) == 1:
            return True

        return False


class Rook(Chessman):
    """Фигура ладья"""

    def __init__(self, color):
        self.color = color
        self.flag = False

    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'R'

    def can_move(self, row, col, row1, col1, field):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""

        if row1 != row and col != col1:
            return False  # можно ходить только по горизонтали или только по вертикали
        if row1 == row and col == col1:
            return False  # нельзя ходить на ту же клетку
        if not self.is_way_clear(row, col, row1, col1, field):
            return False
        return True

    def is_way_clear(self, row, col, row1, col1, board):
        """Проверка, есть ли другие фигуры на пути.
        Фигура на назначенной клетки -- исключение, если она другого цвета"""

        if row1 == row:
            d = int((col - col1) / abs(col - col1))
            for i in range(1, abs(col - col1)):
                if board.field[row1][col - i * d] is not None:
                    return False

        if col1 == col:
            d = int((row - row1) / abs(row - row))
            for i in range(1, abs(row - row1)):
                if field[row - i * d][col1] is not None:
                    return False

        if board.field[row1][col1] is not None:
            if field[row1][col1].get_color() == self.get_color():
                return False
        return True

    def get_flag(self):
        return self.flag


class Queen(Chessman):
    """Фигура ферзь"""

    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'Q'
    
    def can_move(self, row, col, row1, col1, board):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""

        if row1 != row and col != col1 and abs(row1 - row) != abs(col - col1):
            return False  # можно ходить только по горизонтали, или только по вертикали, или только по диагонали
        if row1 == row and col == col1:
            return False  # нельзя ходить на ту же клетку
        if not self.is_way_clear(row1, col1, board.field):
            return False
        return True

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
            for i in range(1, abs(row - row)):
                if field[self.row - i * d][col1] is not None:
                    return False

        if abs(row - row) == abs(col - col):
            d_row = int((row - row1) / abs(row - row1))
            d_col = int((col - col1) / abs(col - col1))
            for i in range(1, abs(row - row1)):
                if field[row - i * d_row][col - i * d_col] is not None:
                    return False

        if field[row1][col1] is not None:
            if field[row1][col1].get_color() == self.get_color():
                return False
        return True


class Bishop(Chessman):
    """Фигура слон"""

    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'B'
    
    def can_move(self, row, col, row1, col1, field):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""

        if abs(row1 - row) != abs(col - col1):
            return False  # можно ходить только по диагонали
        if row1 == row and col == col1:
            return False  # нельзя ходить на ту же клетку
        if not self.is_way_clear(row, col, row1, col1, field):
            return False
        return True

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
    
    def can_move(self, row, col, row1, col1, field):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""

        if not self.is_way_clear(row1, col1, field):
            return False
        if abs(row1 - row) == 2 and abs(col - col1) == 1:
            return True  # можно ходить только буквой Г
        if abs(row1 - row) == 1 and abs(col - col1) == 2:
            return True  # нельзя ходить на ту же клетку
        return False

    def is_way_clear(self, row, col, field):
        """Проверка, есть ли другие фигуры на пути.
        Фигура на назначенной клетки -- исключение, если она другого цвета"""

        if field[row][col] is not None:
            if field[row][col].get_color() == self.get_color():
                return False
        return True


class King(Chessman):
    """Фигура король"""

    def __init__(self, color):
        self.flag = False
        self.color = color

    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'K'
    
    def can_move(self, row, col, row1, col1, board):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""

        field = board.field
        if row1 == row and col == col1:
            return False  # нельзя ходить на ту же клетку
        if abs(row - row1) <= 1 and abs(col - col1) <= 1 and self.is_way_clear(row1, col1, field):
            self.flag = False
            return field
        if col1 - col == 2 and field[row][7] is not None:
            if (not (field[row][7].get_flag() and self.flag) and
                    (field[row][col + 1], field[row][col1]) == (None, None) and
                    not board.is_under_attack(row, col1 - 1, opponent(self.color)) and
                    not board.is_under_attack(row, col1, opponent(self.color))):
                print(5)
                field[row][col1 - 1] = board.field[row][col1 + 1]
                field[row][col1 + 1] = None
                self.flag = True
                return field
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