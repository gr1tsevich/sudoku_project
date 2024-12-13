import tkinter as tk
from menu_backend import MenuBackend

class MenuFrontend:
    """Графический интерфейс для меню Судоку."""

    def __init__(self):
        """
        Инициализирует объект MenuFrontend и создаёт основное окно.

        Args:
            None

        Attributes:
            root (tk.Tk): Основное окно интерфейса.
            backend (MenuBackend): Экземпляр класса MenuBackend для управления логикой меню.
        """
        self.root = tk.Tk()
        self.root.title("Судоку — Меню")
        self.backend = MenuBackend()

    def run(self):
        """
        Запускает интерфейс меню и отображает окно с настройками.

        Метод вызывает create_widgets() для создания виджетов и запускает главный цикл событий.

        Args:
            None

        Returns:
            None
        """
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        """
        Создаёт виджеты для выбора сложности, размера поля и кнопки начала игры.

        Интерфейс включает следующие элементы:
        - Метка для выбора сложности.
        - Переключатели (RadioButton) для выбора уровня сложности ('Легкий', 'Сложный').
        - Метка для выбора размера поля.
        - Переключатели (RadioButton) для выбора размера поля ('4x4', '9x9').
        - Кнопка "Начать игру", которая запускает метод start_game().

        Args:
            None

        Returns:
            None
        """
        tk.Label(self.root, text="Выберите сложность:").pack(pady=5)
        
        self.difficulty_var = tk.StringVar(value="Легкий")
        tk.Radiobutton(self.root, text="Легкий", variable=self.difficulty_var, value="Легкий").pack()
        tk.Radiobutton(self.root, text="Сложный", variable=self.difficulty_var, value="Сложный").pack()

        tk.Label(self.root, text="Выберите размер поля:").pack(pady=5)
        
        self.size_var = tk.StringVar(value="9x9")
        tk.Radiobutton(self.root, text="4x4", variable=self.size_var, value="4x4").pack()
        tk.Radiobutton(self.root, text="9x9", variable=self.size_var, value="9x9").pack()

        tk.Button(self.root, text="Начать игру", command=self.start_game).pack(pady=10)

    def start_game(self):
        """
        Передаёт выбранные настройки в MenuBackend и запускает игру.

        Метод получает значения сложности и размера поля, установленные пользователем, 
        передаёт их в MenuBackend, закрывает окно меню и запускает игру.

        Args:
            None

        Returns:
            None
        """
        difficulty = self.difficulty_var.get()
        size = self.size_var.get()
        self.backend.set_game_settings(difficulty, size)
        self.root.destroy()
        self.backend.start_game()