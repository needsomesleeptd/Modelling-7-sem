import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QPushButton, QLineEdit, QHBoxLayout, QMessageBox, QDialog
)
from collections import Counter
from PyQt6.QtCore import Qt
import numpy as np
MAX_COUNT = 10000
TABLE_PATH = "./digits.txt"

class MyRandom:
    def __init__(self):
        self.current = 1
        self.a = 36261
        self.c = 66037
        self.m = 312500

    def get_number(self, min_number, max_number):
        self.current = (self.a * self.current + self.c) % self.m
        return int(min_number + self.current % (max_number - min_number))

    def calculate_gini_impurity(self, probabilities):
        """Вычисляет нечистоту Джини из распределения вероятностей."""
        return 1 - np.sum(prob ** 2 for prob in probabilities)

    def get_coeff(self, numbers: list, subseq_length: int = 1000):
        """Вычисляет индекс случайности на основе нечистоты Джини и подпоследовательностей."""
        
        #min_value = np.min(numbers)
        #max_value = np.max(numbers)
    
    
        #uniform_distribution = np.linspace(min_value, max_value, len(numbers))

        #mse = np.mean((numbers - uniform_distribution) ** 2 / max(numbers) ** 2)
    
        #return mse
        # Генерация подпоследовательностей
         # Calculate the differences between consecutive elements
        differences = []

        for i in range(1, len(numbers) - 1):
            diff = abs(abs(numbers[i] - numbers[i - 1]) - abs(numbers[i + 1] - numbers[i]))
            differences.append(diff)

        # Calculate the mean of differences
        mean_diff = np.mean(differences)
        dev = np.std(differences)
        if mean_diff == 0 or dev == 0:
            return 0
        print(mean_diff,dev,diff)
    
        return mean_diff / dev 

class ManualInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ручной ввод чисел")
        self.setGeometry(200, 200, 600, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.input_table = QTableWidget(MAX_COUNT, 1)
        self.input_table.setHorizontalHeaderLabels(["Значения"])
        self.layout.addWidget(self.input_table)

        # Button to calculate the coefficient
        self.calculate_button = QPushButton("Рассчитать коэффициент")
        self.calculate_button.clicked.connect(self.calculate_coefficient)
        self.layout.addWidget(self.calculate_button)

        # Label to show metric value
        self.metric_label = QLabel("Коэффициент: — ")
        self.layout.addWidget(self.metric_label)

        # Button to confirm input
        self.confirm_button = QPushButton("Подтвердить ввод")
        self.confirm_button.clicked.connect(self.confirm_input)
        self.layout.addWidget(self.confirm_button)

    def get_manual_numbers(self):
        manual_numbers = []
        for row in range(self.input_table.rowCount()):
            if self.input_table.item(row, 0):
                try:
                    manual_numbers.append(int(self.input_table.item(row, 0).text()))
                except ValueError:
                    QMessageBox.warning(self, "Ошибка ввода", f"Неверный ввод в строке {row + 1}.")
        return manual_numbers

    def calculate_coefficient(self):
        manual_numbers = self.get_manual_numbers()
        if not manual_numbers:
            QMessageBox.warning(self, "Ошибка ввода", "Нет введенных чисел.")
            return
        
        # Calculate and display the coefficient
        coeff = self.parent().random_generator.get_coeff(manual_numbers)
        self.metric_label.setText(f"Коэффициент: {coeff:.4f}")

    def confirm_input(self):
        manual_numbers = self.get_manual_numbers()
        if not manual_numbers:
            QMessageBox.warning(self, "Ошибка ввода", "Нет введенных чисел.")
            return
            
        # Pass numbers to the main window
        coeff = self.parent().random_generator.get_coeff(manual_numbers)
        self.parent().process_manual_input(manual_numbers, coeff)
        self.accept()  # Close dialog after confirmation

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Number Generation")
        self.setGeometry(100, 100, 1000, 600)

        self.layout = QVBoxLayout()
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.create_interface()
        self.random_generator = MyRandom()

    def create_interface(self):
        # Title labels
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("РЕЗУЛЬТАТЫ", alignment=Qt.AlignmentFlag.AlignCenter))
        self.layout.addLayout(title_layout)

        # Shared results table for tabular and algorithmic methods
        self.results_table = QTableWidget(MAX_COUNT, 7)
        self.results_table.setHorizontalHeaderLabels(["№", "1 разряд табл", "2 разряда табл", "3 разряда табл",
                                                      "1 разряд алг", "2 разряда алг", "3 разряда алг"])
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.AllEditTriggers)  # Allow editing
        self.layout.addWidget(self.results_table)

        # Description for coefficients
        self.coeff_description = QLabel("Коэффициенты случайности для каждой таблицы:")
        self.layout.addWidget(self.coeff_description)
        self.coeff_layout = QHBoxLayout()
       
        self.coeff_algo_layout = QVBoxLayout() 
        self.coeff_layout.addLayout(self.coeff_algo_layout)
        self.one_table_entry = QLineEdit()
        self.two_table_entry = QLineEdit()
        self.three_table_entry = QLineEdit()
        self.coeff_algo_layout.addWidget(QLabel("Метрика 1 разряд табл:"))
        self.coeff_algo_layout.addWidget(self.one_table_entry)
        self.coeff_algo_layout.addWidget(QLabel("Метрика 2 разряд табл:"))
        self.coeff_algo_layout.addWidget(self.two_table_entry)
        self.coeff_algo_layout.addWidget(QLabel("Метрика 3 разряд табл:"))
        self.coeff_algo_layout.addWidget(self.three_table_entry)
       
       
        self.coeff_table_layout = QVBoxLayout() 
        self.coeff_layout.addLayout(self.coeff_table_layout)
        self.one_alg_entry = QLineEdit()
        self.two_alg_entry = QLineEdit()
        self.three_alg_entry = QLineEdit()
        self.coeff_table_layout.addWidget(QLabel("Метрика 1 разряд алг:"))
        self.coeff_table_layout.addWidget(self.one_alg_entry)
        self.coeff_table_layout.addWidget(QLabel("Метрика 2 разряд алг:"))
        self.coeff_table_layout.addWidget(self.two_alg_entry)
        self.coeff_table_layout.addWidget(QLabel("Метрика 3 разряд алг:"))
        self.coeff_table_layout.addWidget(self.three_alg_entry)
        
      
        
        
        
       
        
        
        self.layout.addLayout(self.coeff_layout)

        # Button to generate and calculate
        self.solve_button = QPushButton("Сгенерировать случайные числа и рассчитать критерий оценки случайности")
        self.solve_button.clicked.connect(self.solve)
        self.layout.addWidget(self.solve_button)

        # Button to open manual input dialog
        self.manual_button = QPushButton("Учитывать редактирование вручную")
        self.manual_button.clicked.connect(self.open_manual_input_dialog)
        self.layout.addWidget(self.manual_button)

        # Info button about the program
        self.info_button = QPushButton("Информация о программе")
        self.info_button.clicked.connect(self.about_program)
        self.layout.addWidget(self.info_button)

    def about_program(self):
        QMessageBox.information(self, "О программе",
                                "Необходимо разработать графический интерфейс, "
                                "который позволяет сгенерировать последовательность "
                                "псевдослучайных чисел алгоритмическим и табличным "
                                "методами, а также рассчитать коэффициенты их случайности.")

    def get_algo_numbers(self, min_n: int, max_n: int, count: int):
        return [self.random_generator.get_number(min_n, max_n) for _ in range(count)]

    def read_table_numbers(self, filename: str, count):
        numbers = set()

        with open(filename) as file:
            rows = file.readlines()

        for row in rows:
            numbers.update(int(num) for num in row.split()[1:]) # set for randomness
            if len(numbers) >= count:
                break

        numbers = list(numbers)[:count]
        return numbers

    def populate_table_tabular(self, one_digit, two_digit, three_digit):
        for i in range(len(one_digit)):
            self.results_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.results_table.setItem(i, 1, QTableWidgetItem(str(one_digit[i])))
            self.results_table.setItem(i, 2, QTableWidgetItem(str(two_digit[i])))
            self.results_table.setItem(i, 3, QTableWidgetItem(str(three_digit[i])))

    def populate_table_algo(self,one_digit,two_digit, three_digit):
        for i in range(len(one_digit)):
            self.results_table.setItem(i, 4, QTableWidgetItem(str(one_digit[i])))
            self.results_table.setItem(i, 5, QTableWidgetItem(str(two_digit[i])))
            self.results_table.setItem(i, 6, QTableWidgetItem(str(three_digit[i])))
    
    def populate_tables(self,one_digit_table,two_digit_table,three_digit_table,
                       one_digit_alg,two_digit_alg,three_digit_alg):
            self.results_table.clearContents()
            self.populate_table_tabular(one_digit_table,two_digit_table,three_digit_table)
            self.populate_table_algo(one_digit_alg,two_digit_alg,three_digit_alg)
        
    def tabular_solve(self):
        table_nums = self.read_table_numbers(TABLE_PATH, MAX_COUNT * 3)
        one_digit = [table_num % 10 for table_num in table_nums[:MAX_COUNT]]
        two_digits = [(table_num % 100 + 10) if (table_num % 100) < 10 else (table_num % 100)
                      for table_num in table_nums[MAX_COUNT:MAX_COUNT * 2]]
        three_digits = [(table_num % 1000 + 100) if (table_num % 1000) < 100 else (table_num % 1000)
                        for table_num in table_nums[MAX_COUNT * 2:MAX_COUNT * 3]]
        
        return one_digit, two_digits, three_digits

    def algorithmic_solve(self):
        one_digit = self.get_algo_numbers(0, 9, MAX_COUNT)
        two_digits = self.get_algo_numbers(10, 99, MAX_COUNT)
        three_digits = self.get_algo_numbers(100, 999, MAX_COUNT)
        return one_digit, two_digits, three_digits

    def solve(self):
        # Clear results before calculation
        table_one_digit, table_two_digits, table_three_digits = self.tabular_solve()
        algo_one_digit, algo_two_digits, algo_three_digits = self.algorithmic_solve()
        
       
        
        # Populate the results table
        self.populate_tables(table_one_digit, table_two_digits, table_three_digits,algo_one_digit, algo_two_digits, algo_three_digits)

        # Calculate coefficients from the results table
        self.one_alg_entry.setText(str(self.random_generator.get_coeff(algo_one_digit)))
        self.two_alg_entry.setText(str(self.random_generator.get_coeff(algo_two_digits)))
        self.three_alg_entry.setText(str(self.random_generator.get_coeff(algo_three_digits)))

        self.one_table_entry.setText(str(self.random_generator.get_coeff(table_one_digit)))
        self.two_table_entry.setText(str(self.random_generator.get_coeff(table_two_digits)))
        self.three_table_entry.setText(str(self.random_generator.get_coeff(table_three_digits)))
        
        
    def open_manual_input_dialog(self):
        dialog = ManualInputDialog(self)
        dialog.exec()  # Open the dialog as a modal window

    def process_manual_input(self, manual_numbers, coeff):
        try:
            if not manual_numbers:
                raise ValueError("Нет введенных чисел.")
            
            # Extracting digits for display
            one_digit = [numb % 10 for numb in manual_numbers]
            two_digits = [(numb % 100 + 10) for numb in manual_numbers]
            three_digits = [(numb % 1000 + 100) for numb in manual_numbers]

            # Populate the results table with recalculated values
            self.populate_results_table(one_digit, two_digits, three_digits)

            # Update coefficients display
            self.one_alg_entry.setText(str(coeff))  # Use the coefficient calculated in the dialog
            self.two_alg_entry.setText(str(self.random_generator.get_coeff(two_digits)))  # Recalculate for two_digits
            self.three_alg_entry.setText(str(self.random_generator.get_coeff(three_digits)))  # Recalculate for three_digits

        except ValueError as e:
            QMessageBox.warning(self, "Ошибка ввода", f"Пожалуйста, введите корректные числа. {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())