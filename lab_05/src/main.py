from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout
)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont

from generator import Generator
from distribution import EvenDistribution
from processor import Processor
from generator import Generator
from eventModel import EventModel

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа №5 (Разин Андрей ИУ7-74Б)")
        self.setFixedSize(QSize(800, 600))
        self.setStyleSheet("background-color: #e0e0eb;")
        self.operators_interval = []
        self.operators_delta_interval = []
        self.computers = []
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        
        title_font = QFont("Arial", 16, QFont.Weight.Bold)
        
        # Title
        titleLabel = QLabel("ПАРАМЕТРЫ", self)
        titleLabel.setFont(title_font)
        layout.addWidget(titleLabel, 0, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Input Fields with Defaults
        self.countClientsEntry = self.addInputField(layout, "Количество заявок", 1, "300", with_range=False)
        self.intervalEntry = self.addInputField(layout, "Интервал прихода клиента", 2, "10", with_range=True)
        self.intervalDeltaEntry = self.addInputField(layout,"",3,"2",with_range=False)
        self.addOperatorFields(layout, 4)  # Changed to separate method for operators
        
        # Computers
        layout.addWidget(QLabel("КОМПЬЮТЕРЫ", self), 12, 0, 1, 3)
        self.computers.append(self.addComputerField(layout, "Компьютер 1", 13, "15"))
        self.computers.append(self.addComputerField(layout, "Компьютер 2", 14, "30"))

        # РЕЗУЛЬТАТ
        layout.addWidget(QLabel("РЕЗУЛЬТАТ", self), 16, 0, 1, 3)
        self.processed_requests_entry = self.addInputField(layout,"Число обработанных заявок:",16,"")
        self.disposed_requests_entry = self.addInputField(layout,"Число отброшенных заявок:",17,"")
        self.fail_percent = self.addInputField(layout,"Вероятность отказа:",18,"")
        
        
        # Solve Button
        solveButton = QPushButton("Решить", self)
        solveButton.setStyleSheet("background-color: #7575a3; color: white; font-size: 16px;")
        solveButton.clicked.connect(self.solve)
        layout.addWidget(solveButton, 19, 0, 1, 3)

        self.setLayout(layout)

    def addInputField(self, layout, label_text, row, default_text, with_range=False):
        layout.addWidget(QLabel(label_text, self), row, 0)
        entry = QLineEdit(self)
        entry.setText(default_text)
        layout.addWidget(entry, row, 1)

        if with_range:
            layout.addWidget(QLabel("+/-", self), row, 2)
            range_entry = QLineEdit(self)
            range_entry.setText("2")  # Default range value
            layout.addWidget(range_entry, row + 1, 1)

        return entry  # Return the entry for accessing later

    def addOperatorFields(self, layout, start_row):
        layout.addWidget(QLabel("ОПЕРАТОРЫ", self), start_row, 0, 1, 3)
        for i in range(3):
            operator_label = f"Оператор {i + 1}"
            layout.addWidget(QLabel(operator_label, self), start_row + 1 + i * 2, 0)
            operator_entry = QLineEdit(self)
            operator_entry.setText(f"{20 + i * 20}")  # Example default values for operators
            self.operators_interval.append(operator_entry)
            layout.addWidget(operator_entry, start_row + 1 + i * 2, 1)

            layout.addWidget(QLabel("+/-", self), start_row + 1 + i * 2, 2)
            operator_range_entry = QLineEdit(self)
            operator_range_entry.setText(f"{5 + i * 5}")  # Example range values
            self.operators_delta_interval.append(operator_range_entry)
            layout.addWidget(operator_range_entry, start_row + 2 + i * 2, 1)

    def addComputerField(self, layout, label_text, row, default_text):
        layout.addWidget(QLabel(label_text, self), row, 0)
        computer_entry = QLineEdit(self)
        computer_entry.setText(default_text)
        layout.addWidget(computer_entry, row, 1)
        layout.addWidget(QLabel("минут(ы)", self), row, 2)
        return computer_entry

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

    
    
    def getGenerator(self):
        try:
            countClients = int(self.countClientsEntry.text())
            interval = int(self.intervalEntry.text())
            intervalRange = int(self.intervalDeltaEntry.text())
        except:
            self.show_message("Ошибка", 
                "Неверно заданы параметры!\n"
                "Ожидался ввод целых чисел.")
            return

        if countClients <= 0 or interval <= 0 or intervalRange >= interval:
            self.show_message("Ошибка", 
                "Недопустимые значения параметров.")
            return

        return Generator(
                EvenDistribution(interval - intervalRange, interval + intervalRange),
                countClients
            )

    
    def getOperator(self, operatorEntry, operatorRangeEntry):
        try:
            operator = int(operatorEntry.text())
            operatorRange = int(operatorRangeEntry.text())
        except:
            self.show_message("Ошибка", 
                "Неверно заданы значения операторов!\n"
                "Ожидался ввод целых чисел.")
            return

        if operator <= 0 or operatorRange >= operator:
            self.show_message("Ошибка", 
                "Недопустимые значения операторов.")
            return

        return Processor(
                EvenDistribution(operator - operatorRange, operator + operatorRange),
                maxQueue = 1
            )


    def getOperators(self):
        return [self.getOperator(self.operators_interval[0], self.operators_delta_interval[0]),
                self.getOperator(self.operators_interval[1], self.operators_delta_interval[1]),
                self.getOperator(self.operators_interval[2], self.operators_delta_interval[2])]

    
    def getComputer(self, computerEntry):
        try:
            #print(computerEntry.text())
            computer = int(computerEntry.text())
        except:
            self.show_message("Ошибка", 
                "Неверно заданы значения компьютеров!\n"
                "Ожидался ввод целых чисел.")
            return

        if computer <= 0:
            self.show_message("Ошибка", 
                "Недопустимые значения компьютеров.")
            return

        return Processor(
                EvenDistribution(computer, computer),
                maxQueue = -1
            )


    def getComputers(self):
        #print(self.computers)
        return [self.getComputer(self.computers[0]),
                self.getComputer(self.computers[1])]
    
    
    
    def solve(self):
        generators = self.getGenerator()
        operators = self.getOperators()
        computers = self.getComputers()
        event_model = EventModel(generators,operators,computers)
        result = event_model.run()
        self.processed_requests_entry.setText(str(result[0]-1))
        self.disposed_requests_entry.setText(str(result[1]))
        self.fail_percent.setText(str(round(result[2],2)))
        
       

    def about_program(self):
        self.show_message("О программе", "Описание программы...")

if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
