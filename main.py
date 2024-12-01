import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)  # Загрузка интерфейса из main.ui

        # Связываем кнопку с методом обновления данных
        self.refresh_button.clicked.connect(self.load_data)

        # Загрузка данных при старте
        self.load_data()

    def load_data(self):
        # Подключение к базе данных
        connection = sqlite3.connect('123.sqlite')
        cursor = connection.cursor()

        # Выполнение запроса
        query = "SELECT id, name, roast, ground, description, price, volume FROM coffee"
        results = cursor.execute(query).fetchall()

        # Настройка таблицы
        self.tableWidget.setRowCount(len(results))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Name', 'Roast', 'Ground/Beans', 'Description', 'Price', 'Volume']
        )

        # Заполнение таблицы данными
        for row_index, row_data in enumerate(results):
            for column_index, column_data in enumerate(row_data):
                # Преобразование ground в понятный формат
                if column_index == 3:  # Ground/Beans
                    column_data = 'Ground' if column_data else 'Beans'
                self.tableWidget.setItem(row_index, column_index, QTableWidgetItem(str(column_data)))

        # Закрытие соединения
        connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
