import sys
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from PyQt6 import QtWidgets, QtCore

EPS=1e-3

class MatrixInputWidget(QtWidgets.QWidget):
    def __init__(self, size=2):
        super().__init__()
        self.size = size
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.entries = []
        self.create_matrix_input()
        self.fill_random_matrix()

    def create_matrix_input(self):
        # Clear previous entries if any
        for entry in self.entries:
            for widget in entry:
                widget.deleteLater()

        self.entries.clear()

        for i in range(self.size):
            row_entries = []
            for j in range(self.size):
                entry = QtWidgets.QLineEdit()
                entry.setPlaceholderText("0.0")  # Placeholder text
                entry.setStyleSheet("padding: 5px; font-size: 14px;")  # Input field styling
                self.layout.addWidget(entry, i, j)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def fill_random_matrix(self):
        # Fill matrix with random values such that sum of each row = 1
        for i in range(self.size):
            random_values = np.random.rand(self.size)
            normalized_values = random_values / random_values.sum()  # Normalize to sum to 1
            variability = np.random.uniform(0, 0.1, self.size)
            adjusted_values = normalized_values + variability
            adjusted_values /= adjusted_values.sum()  # Normalize again to ensure the sum is exactly 1

            for j in range(self.size):
                self.entries[i][j].setText(f"{adjusted_values[j]:.4f}")

    def validate_matrix(self):
        for i in range(self.size):
            row_sum = sum(float(self.entries[i][j].text()) for j in range(self.size))
            if not np.isclose(row_sum, 1.0, atol=EPS):  # Check if row sum is approximately 1
                return i
        return -1

    def get_matrix(self):
        row_err = self.validate_matrix()
        if row_err != -1:
            raise ValueError(f"Each row must sum up to 1 (error row {row_err}).")
        matrix = np.zeros((self.size, self.size))
        for i in range(self.size):
            for j in range(self.size):
                matrix[i][j] = float(self.entries[i][j].text())
        return matrix

class MatrixInputApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Markov Chain Calculator")
        self.setStyleSheet("background-color: #f0f0f0;")  # Window background color
        self.layout = QtWidgets.QVBoxLayout()

        self.size_label = QtWidgets.QLabel("Enter matrix size (n):")
        self.size_label.setStyleSheet("font-size: 18px;")  # Label styling
        self.layout.addWidget(self.size_label)

        self.size_input = QtWidgets.QSpinBox()
        self.size_input.setMinimum(1)
        self.size_input.setMaximum(20)  # Set maximum matrix size
        self.layout.addWidget(self.size_input)

        self.create_matrix_button = QtWidgets.QPushButton("Create Matrix")
        self.create_matrix_button.setStyleSheet("font-size: 16px;")  # Button styling
        self.create_matrix_button.clicked.connect(self.create_matrix_widget)
        self.layout.addWidget(self.create_matrix_button)

        self.matrix_widget = None  # Placeholder for the matrix widget

        self.calculate_button = QtWidgets.QPushButton("Calculate")
        self.calculate_button.setStyleSheet("font-size: 16px;")  # Button styling
        self.calculate_button.clicked.connect(self.calculate)
        self.layout.addWidget(self.calculate_button)

        # Button for drawing the graph
        self.graph_button = QtWidgets.QPushButton("Draw Probability Graph")
        self.graph_button.setStyleSheet("font-size: 16px;")
        self.graph_button.clicked.connect(self.draw_graph)
        self.layout.addWidget(self.graph_button)

        # Output Fields
        self.probabilities_output = QtWidgets.QTextEdit()
        self.probabilities_output.setReadOnly(True)
        self.probabilities_output.setStyleSheet("font-size: 14px; padding: 5px;")
        self.layout.addWidget(QtWidgets.QLabel("Steady-State Probabilities:"))
        self.layout.addWidget(self.probabilities_output)

        self.times_output = QtWidgets.QTextEdit()
        self.times_output.setReadOnly(True)
        self.times_output.setStyleSheet("font-size: 14px; padding: 5px;")
        self.layout.addWidget(QtWidgets.QLabel("Average Times to Steady State:"))
        self.layout.addWidget(self.times_output)

        self.setLayout(self.layout)

    def create_matrix_widget(self):
        size = self.size_input.value()
        if self.matrix_widget:
            self.matrix_widget.deleteLater()
        self.matrix_widget = MatrixInputWidget(size=size)
        self.layout.addWidget(self.matrix_widget)

    def calculate(self):
        try:
            if not self.matrix_widget:
                raise ValueError("Please create a matrix first.")
            matrix = self.matrix_widget.get_matrix()
        except ValueError as e:
            QtWidgets.QMessageBox.critical(self, "Input Error", str(e))
            return
        
        if np.any(matrix.sum(axis=1) == 0):
            QtWidgets.QMessageBox.critical(self, "Input Error", "Rows must not sum to zero.")
            return

        # Calculate steady-state probabilities
        coefficients = matrix.copy().T
        np.fill_diagonal(coefficients, matrix.diagonal() - matrix.sum(axis=1))
        coefficients[0] = 1  # Normalization condition

        constant_terms = np.zeros(matrix.shape[0])
        constant_terms[0] = 1

        try:
            probabilities = np.linalg.solve(coefficients, constant_terms)
        except np.linalg.LinAlgError:
            QtWidgets.QMessageBox.critical(self, "Calculation Error", "Cannot solve the system of equations.")
            return

        # Calculate average times to steady state
        v = matrix.sum(axis=0) - matrix.diagonal()
        times = probabilities / v

        result_probabilities = "\n".join([f"π[{i + 1}] = {prob:.4f}" for i, prob in enumerate(probabilities)])
        result_times = "\n".join([f"T[{i + 1}] = {time:.4f}" for i, time in enumerate(times)])

        self.probabilities_output.setPlainText(result_probabilities)
        self.times_output.setPlainText(result_times)

    def solve_ode(self, init_probs, _, matrix_coeffs):
        dydt = [0 for _ in range(len(init_probs))]
        for i in range(len(init_probs)):
            dydt[i] = sum(init_probs[j] * matrix_coeffs[i][j] for j in range(len(init_probs)))
        return dydt

    def draw_graph(self):
        try:
            if not self.matrix_widget:
                raise ValueError("Please create a matrix first.")
            matrix = self.matrix_widget.get_matrix()
            steady_probs = self.calculate_steady_state_probabilities(matrix)
            self.plot_probabilities(steady_probs, matrix)
        except ValueError as e:
            QtWidgets.QMessageBox.critical(self, "Input Error", str(e))

    def calculate_steady_state_probabilities(self, matrix):
        coefficients = matrix.copy().T
        np.fill_diagonal(coefficients, matrix.diagonal() - matrix.sum(axis=1))
        coefficients[0] = 1
        
        constant_terms = np.zeros(matrix.shape[0])
        constant_terms[0] = 1
        
        probabilities = np.linalg.solve(coefficients, constant_terms)
        return probabilities

    def plot_probabilities(self, steady_probs, matrix):
        matrix_coeffs = [
            [-sum(matrix[i]) + matrix[i][j] if j == i else matrix[j][i]
             for j in range(matrix.shape[0])]
            for i in range(matrix.shape[0])
        ]

        times = np.linspace(0, 20, 100)  # Time range for plotting
        init_probs = [1] + [0] * (len(steady_probs) - 1)  # Initial uniform distribution
        res_ode = odeint(self.solve_ode, init_probs, times, args=(matrix_coeffs,))
        res_ode = np.transpose(res_ode)

        for i in range(len(res_ode)):
            plt.plot(times, res_ode[i], label=f"p[{i}]")

        plt.legend()
        plt.xlabel("Time")
        plt.ylabel("Probability")
        plt.title("Time Evolution of State Probabilities")
        plt.grid()
        plt.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MatrixInputApp()
    window.show()
    sys.exit(app.exec())