from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QWidget, QMessageBox
)
import sys
from distribution import PoissonDistribution, UniformDistribution
from event_model import eventModel
from step_model import stepModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Имитационная Модель")
        self.setGeometry(100, 100, 400, 400)  # Установка размера окна (x, y, width, height)

        # Initialize input fields with labels
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Равномерный закон распределения"))
        self.a_label = QLabel("a (число):", self)
        self.a_input = QLineEdit(self)
        self.a_input.setPlaceholderText("Введите a (число)")
        self.a_input.setText("1.0")

        self.b_label = QLabel("b (число):", self)
        self.b_input = QLineEdit(self)
        self.b_input.setPlaceholderText("Введите b (число)")
        self.b_input.setText("5.0")

        layout.addWidget(self.a_label)
        layout.addWidget(self.a_input)
        layout.addWidget(self.b_label)
        layout.addWidget(self.b_input)

        layout.addWidget(QLabel("Закон распределения Пуассона"))
        self.lambda_label = QLabel("λ (положительное число):", self)
        self.lambda_input = QLineEdit(self)
        self.lambda_input.setPlaceholderText("Введите λ (положительное число)")
        self.lambda_input.setText("2.5")

        layout.addWidget(self.lambda_label)
        layout.addWidget(self.lambda_input)

        layout.addWidget(QLabel("Время дельта для протяжки:"))
        self.delta_t_input = QLineEdit(self)
        self.delta_t_input.setPlaceholderText("Введите delta_t (число)")
        self.delta_t_input.setText("0.1")
        layout.addWidget(self.delta_t_input)

        layout.addWidget(QLabel("Вероятность возврата заявки:"))
        self.repeat_prob_input = QLineEdit(self)
        self.repeat_prob_input.setPlaceholderText("Введите repeat_prob (число)")
        self.repeat_prob_input.setText("0.0")
        layout.addWidget(self.repeat_prob_input)

        layout.addWidget(QLabel("Число заявок для обработки:"))
        self.max_tasks_input = QLineEdit(self)
        self.max_tasks_input.setPlaceholderText("Введите число заявок (max_tasks)")
        self.max_tasks_input.setText("10000")
        layout.addWidget(self.max_tasks_input)

        # Solve button
        self.solve_button = QPushButton("Решить", self)
        self.solve_button.clicked.connect(self.solve)
        layout.addWidget(self.solve_button)

        self.result_label = QLabel("Макс. длина очереди при использовании событийного принципа: ", self)
        self.result_label_delta = QLabel("Макс. длина очереди при использовании принципа Δt: ", self)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_label_delta)

        # Container setup
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def solve(self):
        try:
            a = float(self.a_input.text())
            b = float(self.b_input.text())
            lambda_ = float(self.lambda_input.text())
            delta_t = float(self.delta_t_input.text())
            repeat_prob = float(self.repeat_prob_input.text())
            max_tasks = int(self.max_tasks_input.text())

            if a >= b:
                raise ValueError("a должно быть меньше b")

            generator = UniformDistribution(a, b)
            processor = PoissonDistribution(k=1,lambda_=lambda_)  # Убираем k

            max_len_event = eventModel(generator, processor, max_tasks, repeat_prob)
            max_len_delta = stepModel(generator, processor, max_tasks, repeat_prob, delta_t)

            self.result_label.setText(f"Макс. длина очереди при использовании событийного принципа: {max_len_event:.6f}")
            self.result_label_delta.setText(f"Макс. длина очереди при использовании принципа Δt: {max_len_delta:.6f}")

        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))

# Main application execution
app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())