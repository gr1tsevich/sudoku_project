"""
Запуск основного приложения.

Импортируется класс MenuFrontend из модуля menu_frontend. 
Затем создаётся экземпляр класса MenuFrontend и вызывается его метод run(), 
который отвечает за отображение главного меню и запуск приложения.

Args:
    None

Returns:
    None
"""
from menu_frontend import MenuFrontend

if __name__ == "__main__":
    app = MenuFrontend()
    app.run()