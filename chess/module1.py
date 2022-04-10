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

    def __init__(self, row, col, color):
        self.set_position(row, col)
        self.color = color

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
        #for j in range(8): # все пешки
        #    self.field[1][j] = Pawn(1, j, WHITE)
        #    self.field[6][j] = Pawn(6, j, BLACK)
        for i in range(2): # остальные фигуры
            # при i = 0 сначала выставляются фигуры на левой половине доски,
            # при i = 1 на правой
            self.field[0][7 * i] = Rook(0, 7 * i, WHITE) 
            self.field[7][7 * i] = Rook(7, 7 * i, BLACK)
            self.field[0][1 + 5 * i] = Knight(0, 1 + 5 * i, WHITE) 
            self.field[7][1 + 5 * i] = Knight(7, 1 + 5 * i, BLACK)
            self.field[0][2 + 3 * i] = Bishop(0, 2 + 3 * i, WHITE) 
            self.field[7][2 + 3 * i] = Bishop(7, 2 + 3 * i, BLACK)
        self.field[7][3] = Queen(7, 3, BLACK)
        self.field[0][3] = Queen(0, 3, WHITE)
        self.field[7][4] = King(7, 4, BLACK)
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

            piece.set_position(row1, col1)  # обновляем информацию о фигуре
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
            flag = piece.can_move(row1, col1, self.is_can_be_taken_on_pass, self.field)
            # flag = (bool, bool) 
            # первое - возможен ли ход
            # второе - было ли это взятием на проходе
            if not flag[0]:  # ход не возможен по любой из причин
                return False
            if flag[1]:
                # пешка ловит на проходе,
                # поэтому следует убрать пойманную пешку с доски
                self.field[self.is_can_be_taken_on_pass[2]][self.is_can_be_taken_on_pass[3]]
                # иначе пешка просто ходит или ест другую фигуру,
                # никаких дополнительных действий не нужно

        if not piece.can_move(row1, col1, self.field):
            return False  # выбранная фигура не может походить в выбранную клетку

        # если данный ход ставит своего же короля под удар, вернуть False. Не реализовано
        # если королю шах, и выбранная фигура не король, вернуть False. Не реализовано

        if isinstance(piece, King) and self.is_under_attack(row, col, opponent(self.current_player_color())):
            return False  # Нельзя ходить королём на клетки, которые бьются другими фигурами.
        return True

    def is_under_attack(self, row, col, color):
        """Проверка, находится ли данная клетка под атакой других фигур данного цвета"""

        for i, j in range((8, 8)):
            if self.field is not None:
                piece = self.field[i][j]
                if color == piece.get_color():
                    if isinstance(piece, Pawn):  # у пешки немного отличающаяся система хода, проверяем её отдельно от других фигур
                        if piece.can_move(row, col, self.is_can_be_taken_on_pass, self.field):
                            return True
                    if piece.can_move(row, col, self.field):
                        return True


class Pawn(Chessman):
    """Фигура пешка"""

    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'P'

    def can_move(self, row, col, is_can_be_taken_on_pass, field):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""
        return True


class Rook(Chessman):
    """Фигура ладья"""

    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'R'

    def can_move(self, row, col, field):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""

        if row != self.row and self.col != col:
            return False  # можно ходить только по горизонтали или только по вертикали
        if row == self.row and self.col == col:
            return False  # нельзя ходить на ту же клетку
        if not self.is_way_clear(row, col, field):
            return False
        return True

    def is_way_clear(self, row, col, field):
        """Проверка, есть ли другие фигуры на пути.
        Фигура на назначенной клетки -- исключение, если она другого цвета"""

        if row == self.row:
            d = int((self.col - col) / abs(self.col - col))
            for i in range(1, abs(self.col - col)):
                if field[row][self.col - i * d] is not None:
                    return False

        if col == self.col:
            d = int((self.row - row) / abs(self.row - row))
            for i in range(1, abs(self.row - row)):
                if field[self.row - i * d][col] is not None:
                    return False

        if field[row][col] is not None:
            if field[row][col].get_color() == self.get_color():
                return False
        return True
 
class Queen(Chessman):
    """Фигура ферзь"""

    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'Q'
    
    def can_move(self, row, col):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""
        return True


class Bishop(Chessman):
    """Фигура слон"""

    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'B'
    
    def can_move(self, row, col, field):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""

        if abs(row - self.row) != abs(self.col - col):
            return False  # можно ходить только по диагонали
        if row == self.row and self.col == col:
            return False  # нельзя ходить на ту же клетку
        if not self.is_way_clear(row, col, field):
            return False
        return True

    def is_way_clear(self, row, col, field):
        """Проверка, есть ли другие фигуры на пути.
        Фигура на назначенной клетки -- исключение, если она другого цвета"""
        
        d_row = int((self.row - row) / abs(self.row - row))
        d_col = int((self.col - col) / abs(self.col - col))
        for i in range(1, abs(self.row - row)):
            if field[self.row - i * d_row][self.col - i * d_col] is not None:
                return False

        if field[row][col] is not None:
            if field[row][col].get_color() == self.get_color():
                return False
        return True


class Knight(Chessman):
    """Фигура конь"""
    
    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'N'
    
    def can_move(self, row, col, field):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""

        if not self.is_way_clear(row, col, field):
            return False
        if abs(row - self.row) == 2 and abs(self.col - col) == 1:
            return True  # можно ходить только буквой Г
        if abs(row - self.row) == 1 and abs(self.col - col) == 2:
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

    def char(self):
        """Функция, возвращающая имя фигуры"""
        return 'K'
    
    def can_move(self, row, col):
        """Функция, проверяющая, может ли данная фигура походить на данную клетку"""
        return True


if __name__ == "__main__":
    main()
