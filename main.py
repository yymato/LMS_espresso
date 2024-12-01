import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog

class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.load_data()
        self.refresh_button.clicked.connect(self.load_data)

        # Кнопка добавления нового кофе
        self.add_button.clicked.connect(self.add_new_coffee)

        # Кнопка редактирования выбранной записи
        self.edit_button.clicked.connect(self.edit_selected_coffee)

    def load_data(self):
        connection = sqlite3.connect('123.sqlite')
        cursor = connection.cursor()

        query = "SELECT id, name, roast, ground, description, price, volume FROM coffee"
        results = cursor.execute(query).fetchall()

        self.tableWidget.setRowCount(len(results))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Name', 'Roast', 'Ground/Beans', 'Description', 'Price', 'Volume']
        )

        for row_index, row_data in enumerate(results):
            for column_index, column_data in enumerate(row_data):
                if column_index == 3:  # Преобразуем ground в текст
                    column_data = 'Ground' if column_data else 'Beans'
                self.tableWidget.setItem(row_index, column_index, QTableWidgetItem(str(column_data)))

        connection.close()

    def add_new_coffee(self):
        # Открываем форму для добавления нового кофе
        dialog = AddEditCoffeeForm(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    def edit_selected_coffee(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            coffee_id = self.tableWidget.item(selected_row, 0).text()

            connection = sqlite3.connect('123.sqlite')
            cursor = connection.cursor()
            query = f"SELECT * FROM coffee WHERE id = {coffee_id}"
            cursor.execute(query)
            coffee_data = cursor.fetchone()

            dialog = AddEditCoffeeForm(self, coffee_data)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.load_data()

            connection.close()

class AddEditCoffeeForm(QDialog):
    def __init__(self, parent=None, coffee_data=None):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)

        self.cooffee_data = coffee_data
        if coffee_data:
            self.populate_fields(coffee_data)

        self.buttonBox.accepted.connect(self.save_data)
        self.buttonBox.rejected.connect(self.reject)

    def populate_fields(self, coffee_data):
        self.nameLineEdit.setText(coffee_data[1])
        self.roastComboBox.setCurrentText(coffee_data[2])
        self.groundComboBox.setCurrentIndex(0 if coffee_data[3] == 0 else 1)
        self.descriptionTextEdit.setPlainText(coffee_data[4])
        self.priceSpinBox.setValue(int(coffee_data[5]))
        self.volumeSpinBox.setValue(int(coffee_data[6]))

    def save_data(self):
        name = self.nameLineEdit.text()
        roast = self.roastComboBox.currentText()
        ground = 0 if self.groundComboBox.currentIndex() == 0 else 1
        description = self.descriptionTextEdit.toPlainText()
        price = self.priceSpinBox.value()
        volume = self.volumeSpinBox.value()

        connection = sqlite3.connect('123.sqlite')
        cursor = connection.cursor()

        if self.cooffee_data:
            coffee_id = self.cooffee_data[0]
            query = """
                UPDATE coffee
                SET name = ?, roast = ?, ground = ?, description = ?, price = ?, volume = ?
                WHERE id = ?
            """
            cursor.execute(query, (name, roast, ground, description, price, volume, coffee_id))
        else:
            query = """
                INSERT INTO coffee (name, roast, ground, description, price, volume)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (name, roast, ground, description, price, volume))

        connection.commit()
        connection.close()
        self.accept()

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
