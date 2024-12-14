"""
Класс SudokuGenerator используется для генерации головоломок Судоку заданного размера и сложности.

Этот класс создаёт полностью решённую сетку и затем удаляет из неё числа для формирования задачи Судоку.

Attributes:
    size (int): Размер сетки (например, 4 или 9).
    region_size (int): Размер подрегиона (2 для 4x4, 3 для 9x9).
    grid (list[list[int]]): Сетка с текущей версией головоломки Судоку.
    solved_grid (list[list[int]]): Полностью решённая версия сетки Судоку.

Methods:
    generate(difficulty):
        Генерирует головоломку Судоку заданного уровня сложности.
    
    _fill_grid():
        Заполняет сетку числами, чтобы получить полностью решённую версию Судоку.
    
    _remove_numbers(difficulty):
        Удаляет случайные числа из сетки, чтобы создать головоломку с пробелами.
    
    _is_valid_placement(row, col, num):
        Проверяет, можно ли вставить число в указанную ячейку сетки.
    
    _solve():
        Использует метод backtracking для решения сетки Судоку.
    
    _find_empty_cell():
        Ищет первую пустую ячейку (со значением 0) и возвращает её координаты.
"""
import random

class SudokuGenerator:
    """Класс для генерации и создания головоломок Судоку."""
    def __init__(self, size):
        """
        Инициализирует генератор Судоку.

        Args:
            size (int): Размер сетки (например, 4 для 4x4 или 9 для 9x9).
        
        Attributes:
            size (int): Размер сетки.
            region_size (int): Размер подрегиона (2 для 4x4, 3 для 9x9).
            grid (list[list[int]]): Сетка с текущей версией головоломки Судоку.
            solved_grid (list[list[int]]): Полностью решённая версия сетки.
        """
        self.size = size
        self.region_size = int(size ** 0.5)
        self.grid = [[0] * size for _ in range(size)]
        self.solved_grid = []   

    def generate(self, difficulty):
        """
        Генерирует головоломку Судоку с заданным уровнем сложности.

        Заполняет сетку полностью и затем удаляет из неё числа в зависимости от сложности.

        Args:
            difficulty (str): Уровень сложности ('Легкий', 'Средний' или 'Сложный').

        Returns:
            list[list[int]]: Двумерный массив с частично заполненной сеткой Судоку.
        """
        self._fill_grid()  # Полностью заполняем судоку (полная версия)
        self.solved_grid = [row[:] for row in self.grid]  # Сохраняем решённую версию
        self._remove_numbers(difficulty)  # Удаляем числа в зависимости от сложности
        return self.grid

    def _fill_grid(self):
        """
        Заполняет сетку числами, чтобы получить полностью решённую версию Судоку.

        Используется метод backtracking для заполнения всех ячеек сетки.
        
        Returns:
            None
        """
        self._solve()

    def _remove_numbers(self, difficulty):
        """
        Удаляет случайные числа из сетки для создания головоломки Судоку.

        Количество удаляемых чисел зависит от сложности:
        - Легкий: удаляется половина всех ячеек.
        - Сложный: удаляется 2/3 всех ячеек.

        Args:
            difficulty (str): Уровень сложности ('Легкий' или 'Сложный').

        Returns:
            None
        """
        total_cells = self.size * self.size
        cells_to_remove = total_cells // 2 if difficulty == 'Легкий' else total_cells * 2 // 3
        
        for _ in range(cells_to_remove):
            while True:
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - 1)
                if self.grid[row][col] != 0:
                    self.grid[row][col] = 0
                    break

    def _is_valid_placement(self, row, col, num):
        """
        Проверяет, можно ли поместить число в указанную ячейку сетки.

        Проверяется строка, столбец и подрегион, чтобы убедиться, что число отсутствует в них.

        Args:
            row (int): Номер строки ячейки.
            col (int): Номер столбца ячейки.
            num (int): Число, которое нужно вставить в ячейку.

        Returns:
            bool: True, если число можно вставить в ячейку; иначе False.
        """
        if num in self.grid[row]: #проверка строки
            return False

        if num in (self.grid[i][col] for i in range(self.size)): #проверка столбца
            return False

        region_start_row = (row // self.region_size) * self.region_size 
        region_start_col = (col // self.region_size) * self.region_size

        for i in range(self.region_size): # Проверка подрегиона
            for j in range(self.region_size):
                if self.grid[region_start_row + i][region_start_col + j] == num:
                    return False

        return True

    def _solve(self):
        """
        Решает сетку Судоку с использованием метода backtracking.

        Идею с методом backtracking взял с сайта https://medium.com/swlh/sudoku-solver-using-backtracking-in-python-8b0879eb5c2d
        
        Используется для заполнения пустой сетки Судоку числами.

        Returns:
            bool: True, если Судоку решена; False, если решение не найдено.
        """
        empty_cell = self._find_empty_cell()
        if not empty_cell:
            return True  # Нет пустых клеток — судоку решено

        row, col = empty_cell
        numbers = list(range(1, self.size + 1))
        random.shuffle(numbers) # Перемешиваем числа, чтобы получить случайное заполнение

        for num in numbers:
            if self._is_valid_placement(row, col, num):
                self.grid[row][col] = num  # Пробуем поставить число
                if self._solve():  # Рекурсия
                    return True
                self.grid[row][col] = 0  # Откат значения

        return False

    def _find_empty_cell(self):
        """
        Ищет первую пустую ячейку (со значением 0) в сетке.

        Метод используется для поиска незаполненных ячеек для метода backtracking.

        Returns:
            tuple[int, int] | None: Координаты ячейки (row, col), если найдена пустая ячейка; иначе None.
        """
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    return row, col
        return None
