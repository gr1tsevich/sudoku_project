"""
Класс GameFrontend предоставляет графический интерфейс для игры Судоку, позволяя пользователю
вводить числа в ячейки, получать подсказки и проверять правильность заполнения сетки.

Этот класс отвечает за визуальное отображение сетки Судоку и обработку пользовательского ввода.

Attributes:
    root (tk.Tk): Главное окно приложения.
    backend (GameBackend): Объект, управляющий логикой игры.
    size (int): Размер сетки (например, 4 или 9).
    entries (list[list[tk.Entry]]): Список виджетов ввода для каждой ячейки сетки.
    hint_button (tk.Button): Кнопка для получения подсказок.

Methods:
    run():
        Запускает главный цикл интерфейса.
    
    create_widgets():
        Создаёт виджеты интерфейса для отображения сетки и кнопок управления.
    
    validate_input(event, row, col):
        Проверяет правильность ввода пользователя и подсвечивает ошибки.
    
    check_victory():
        Проверяет, заполнена ли сетка правильно, и отображает сообщение о победе.
    
    lock_board():
        Блокирует все ячейки после завершения игры.
    
    get_hint():
        Выбирает случайную пустую ячейку и заполняет её правильным значением.
"""
import tkinter as tk
from tkinter import messagebox
from game_backend import GameBackend

class GameFrontend:
    """Класс для визуализации интерфейса Судоку и обработки пользовательского ввода.""" 
    def __init__(self, difficulty, size):
        """
        Инициализирует интерфейс для игры Судоку.

        Args:
            difficulty (str): Уровень сложности игры.
            size (str): Размер сетки Судоку (например, '4x4' или '9x9').

        Attributes:
            root (tk.Tk): Главное окно приложения.
            backend (GameBackend): Объект, управляющий логикой игры.
            size (int): Размер сетки Судоку (4 или 9).
            entries (list[list[tk.Entry]]): Список виджетов ввода для каждой ячейки сетки.
            hint_button (tk.Button): Кнопка для получения подсказок.
        """
        self.root = tk.Tk()
        self.root.title(f"Судоку {size} — {difficulty}")
        self.backend = GameBackend(difficulty, size)
        self.size = int(size.split('x')[0])
        self.entries = []  # Матрица виджетов ввода для каждой ячейки
        self.hint_button = None  # Кнопка подсказки

    def run(self):
        """Запускает главный цикл интерфейса."""
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        """
        Создаёт виджеты интерфейса для отображения сетки и кнопок управления.

        Формирует сетку ячеек Судоку и элементы управления, такие как кнопка подсказки.

        Returns:
            None
        """
        self.entries = [[None for _ in range(self.size)] for _ in range(self.size)]

        # Главный контейнер с рамкой для всей сетки
        grid_frame = tk.Frame(self.root, bg="grey", relief="solid", bd=2)
        grid_frame.pack(padx=10, pady=10)

        block_size = 2 if self.size == 4 else 3  # Размер района (блока)

        # Создаём сетку районов (2x2 для 4x4, 3x3 для 9x9)
        for block_row in range(0, self.size, block_size):
            for block_col in range(0, self.size, block_size):
                # Обрамление района
                block_frame = tk.Frame(grid_frame, bg="black", relief="solid", bd=2)
                block_frame.grid(row=block_row // block_size, column=block_col // block_size, padx=1, pady=1)

                # Создаём ячейки внутри района
                for row in range(block_size):
                    for col in range(block_size):
                        cell_row = block_row + row
                        cell_col = block_col + col

                        entry = tk.Entry(block_frame, width=2, justify='center', font=('Arial', 16), relief='solid', bd=0)
                        entry.grid(row=row, column=col, padx=1, pady=1)

                        # Если в ячейке есть значение, блокируем её
                        if self.backend.sudoku_grid[cell_row][cell_col] != 0:
                            entry.insert(0, self.backend.sudoku_grid[cell_row][cell_col])
                            entry.config(state='disabled', disabledbackground='lightgray', disabledforeground='black')
                        else:
                            entry.bind('<KeyRelease>', lambda event, r=cell_row, c=cell_col: self.validate_input(event, r, c))

                        self.entries[cell_row][cell_col] = entry

        # Кнопка подсказки
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.hint_button = tk.Button(button_frame, text="Подсказка (3)", font=('Arial', 12), command=self.get_hint, bg='lightblue', relief='raised', bd=2)
        self.hint_button.pack()

    def validate_input(self, event, row, col):
        """
        Проверяет правильность ввода пользователя и подсвечивает ошибки.

        Принимает ввод пользователя и проверяет, можно ли вставить это число в ячейку.
        Подсвечивает ошибочные значения красным фоном.

        Args:
            event (tk.Event): Событие ввода.
            row (int): Номер строки ячейки.
            col (int): Номер столбца ячейки.

        Returns:
            None
        """
        entry = self.entries[row][col]
        value = entry.get()

        if not value.isdigit():
            entry.delete(0, tk.END)
            return

        num = int(value)

        if num < 1 or num > self.size:
            entry.delete(0, tk.END)
            return

        is_valid = self.backend.is_valid_move(row, col, num)
        if is_valid:
            entry.config(bg='white')
            self.backend.user_grid[row][col] = num
        else:
            entry.config(bg='red')

        self.check_victory()

    def check_victory(self):
        """
        Проверяет, заполнена ли сетка корректно, и отображает сообщение о победе.

        Если пользователь заполнил сетку корректно, появляется сообщение о победе, 
        и все ячейки блокируются.

        Returns:
            None
        """
        if self.backend.is_game_complete():
            messagebox.showinfo("Поздравляем!", "Вы успешно завершили судоку!")
            self.lock_board()

    def lock_board(self):
        """
        Блокирует все ячейки после завершения игры.

        Блокирует все ячейки, чтобы предотвратить дальнейший ввод после победы.

        Returns:
            None
        """
        for row in range(self.size):
            for col in range(self.size):
                entry = self.entries[row][col]
                entry.config(state='disabled')

    def get_hint(self):
        """
        Предоставляет пользователю подсказку, вставляя правильное значение в случайную пустую ячейку.

        Выбирает случайную пустую ячейку и вставляет туда правильное значение.
        Подсказки ограничены количеством (не более 3 за игру). 
        После использования всех подсказок кнопка отключается.

        Returns:
            None
        """
        hint = self.backend.get_hint()
        if hint:
            row, col, value = hint
            entry = self.entries[row][col]
            entry.delete(0, tk.END)
            entry.insert(0, value)
            entry.config(state='disabled')

            hints_left = 3 - self.backend.hint_count
            self.hint_button.config(text=f"Подсказка ({hints_left})")

            if hints_left == 0:
                self.hint_button.config(state='disabled')
        if self.backend.is_game_complete():
            messagebox.showinfo("Поздравляем!", "Вы успешно решили Судоку!")
            self.root.quit()  # Закрыть игру