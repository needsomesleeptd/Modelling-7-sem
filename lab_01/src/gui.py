import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QSlider, QFormLayout, QPushButton, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from scipy.stats import poisson, uniform
import pyqtgraph as pg


class UniformDistributionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Uniform Distribution Plotter")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)

        # Create the plot widget for density and distribution
        self.plot_widget_dist_dens = pg.PlotWidget()
        self.plot_widget_dist = pg.PlotWidget()
        
        self.layout.addWidget(self.plot_widget_dist_dens)
        self.layout.addWidget(self.plot_widget_dist)

        # Initial parameters
        self.uniform_low = 0
        self.uniform_high = 10
        self.x_start = 0
        self.x_end = 10
        self.update_plot()

        # Add sliders and input fields for Uniform distribution parameters
        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.uniform_low_slider = QSlider(Qt.Orientation.Horizontal)
        self.uniform_low_slider.setMinimum(0)
        self.uniform_low_slider.setMaximum(10)
        self.uniform_low_slider.setValue(self.uniform_low)
        self.uniform_low_slider.valueChanged.connect(self.update_uniform_params)
        self.form_layout.addRow("Параметр a:", self.uniform_low_slider)

        self.uniform_low_input = QLineEdit()
        self.uniform_low_input.setText(str(self.uniform_low))
        self.uniform_low_input.textChanged.connect(self.update_uniform_low_input)
        self.form_layout.addRow("Параметр a:", self.uniform_low_input)

        self.uniform_high_slider = QSlider(Qt.Orientation.Horizontal)
        self.uniform_high_slider.setMinimum(10)
        self.uniform_high_slider.setMaximum(20)
        self.uniform_high_slider.setValue(self.uniform_high)
        self.uniform_high_slider.valueChanged.connect(self.update_uniform_params)
        self.form_layout.addRow("Параметр b:", self.uniform_high_slider)

        self.uniform_high_input = QLineEdit()
        self.uniform_high_input.setText(str(self.uniform_high))
        self.uniform_high_input.textChanged.connect(self.update_uniform_high_input)
        self.form_layout.addRow("Параметр b:", self.uniform_high_input)

        # Add x axis start and end inputs
        self.x_start_input = QLineEdit()
        self.x_start_input.setText(str(self.x_start))
        self.x_start_input.textChanged.connect(self.update_x_start)
        self.form_layout.addRow("X начальное:", self.x_start_input)

        self.x_end_input = QLineEdit()
        self.x_end_input.setText(str(self.x_end))
        self.x_end_input.textChanged.connect(self.update_x_end)
        self.form_layout.addRow("X конечное:", self.x_end_input)

        # Button to switch to Poisson distribution window
        self.switch_button = QPushButton("Перейти на распределение Пуассона")
        self.switch_button.clicked.connect(self.open_poisson_window)
        self.layout.addWidget(self.switch_button)

    def show_error(self, message):
        QMessageBox.critical(self, 'Ошибка ввода', message)

    def update_uniform_params(self):
        self.uniform_low = self.uniform_low_slider.value()
        self.uniform_high = self.uniform_high_slider.value()
        self.uniform_low_input.setText(str(self.uniform_low))
        self.uniform_high_input.setText(str(self.uniform_high))
        self.update_plot()

    def update_uniform_low_input(self):
        try:
            val = float(self.uniform_low_input.text())
            if val > self.uniform_high:
                self.show_error("Параметр распределения a должен быть меньше b")
                return
            self.uniform_low = val
            self.uniform_low_slider.setValue(int(val))
            self.update_plot()
        except ValueError:
             self.show_error("Невалидный ввод a")

    def update_uniform_high_input(self):
        try:
            val = float(self.uniform_high_input.text())
            if val < self.uniform_low:
                self.show_error("Параметр распределения a должен быть меньше b")
                return
            self.uniform_high = val
            self.uniform_high_slider.setValue(int(val))
            self.uniform_low_slider.setMaximum(int(val))
            self.update_plot()
        except ValueError:
            self.show_error("Невалидный ввод b")

    def update_x_start(self):
        try:
            self.x_start = float(self.x_start_input.text())
            self.uniform_high_slider.setMinimum(int(self.x_start))
            self.uniform_low_slider.setMinimum(int(self.x_start)) 
            self.update_plot()
        except ValueError:
           self.show_error("Невалидный ввод конца X")

    def update_x_end(self):
        try:
            self.x_end = float(self.x_end_input.text())
            self.uniform_high_slider.setMaximum(int(self.x_end))
            self.uniform_low_slider.setMaximum(int(self.x_end)) 
            self.update_plot()
        except ValueError:
            self.show_error("Невалидный ввод начала X")

    def update_plot(self):
        self.plot_widget_dist_dens.clear()
        self.plot_widget_dist.clear()
        uniform_x = np.linspace(self.x_start, self.x_end, 100)
        uniform_pdf = uniform.pdf(uniform_x, self.uniform_low, self.uniform_high - self.uniform_low)
        uniform_cdf = uniform.cdf(uniform_x, self.uniform_low, self.uniform_high - self.uniform_low)

        self.plot_widget_dist_dens.plot(uniform_x, uniform_pdf, pen='b', name='Функция плотности равномерного распределения')
        self.plot_widget_dist.plot(uniform_x, uniform_cdf, pen='r', name="Функция равномерного распределения")

    def open_poisson_window(self):
        self.poisson_window = PoissonDistributionWindow()
        self.poisson_window.show()
        self.close()


class PoissonDistributionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Poisson Distribution Plotter")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)

        # Create the plot widget for PMF and CDF
        self.plot_widget_pmf = pg.PlotWidget()
        self.plot_widget_cdf = pg.PlotWidget()

        self.layout.addWidget(self.plot_widget_pmf)
        self.layout.addWidget(self.plot_widget_cdf)

        self.poisson_lambda = 5
        self.x_start = 0
        self.x_end = 20
        self.update_plot()

        # Add sliders and input fields for Poisson distribution parameters
        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.poisson_slider = QSlider(Qt.Orientation.Horizontal)
        self.poisson_slider.setMinimum(1)
        self.poisson_slider.setMaximum(20)
        self.poisson_slider.setValue(self.poisson_lambda)
        self.poisson_slider.valueChanged.connect(self.update_poisson_param)
        self.form_layout.addRow("Параметр λ:", self.poisson_slider)

        self.poisson_input = QLineEdit()
        self.poisson_input.setText(str(self.poisson_lambda))
        self.poisson_input.textChanged.connect(self.update_poisson_input)
        self.form_layout.addRow("Параметр λ :", self.poisson_input)

        # Add x axis start and end inputs
        self.x_start_input = QLineEdit()
        self.x_start_input.setText(str(self.x_start))
        self.x_start_input.textChanged.connect(self.update_x_start)
        self.form_layout.addRow("X начальное:", self.x_start_input)

        self.x_end_input = QLineEdit()
        self.x_end_input.setText(str(self.x_end))
        self.x_end_input.textChanged.connect(self.update_x_end)
        self.form_layout.addRow("X конечное:", self.x_end_input)

        # Button to switch to Uniform distribution window
        self.switch_button = QPushButton("Перейти на равномерное распределение")
        self.switch_button.clicked.connect(self.open_uniform_window)
        self.layout.addWidget(self.switch_button)

    def show_error(self, message):
        QMessageBox.critical(self, 'Ошибка ввода', message)

    def update_poisson_param(self):
        self.poisson_lambda = self.poisson_slider.value()
        self.poisson_input.setText(str(self.poisson_lambda))
        self.update_plot()

    def update_poisson_input(self):
        try:
            val = float(self.poisson_input.text())
            if val < 0:
                self.show_error("λ должна быть > 0 ")
            self.poisson_lambda = val
            self.poisson_slider.setValue(int(val))
            self.update_plot()
        except ValueError:
            self.show_error("Невалидное значение λ")

    def update_x_start(self):
        try:
            self.x_start = float(self.x_start_input.text())
            if self.x_start > self.x_end:
                self.show_error("Начальное значение X отображения должно быть больше конечного")
            self.update_plot()
        except ValueError:
            self.show_error("Невалидное значение для начального отображения X")

    def update_x_end(self):
        try:
            self.x_end = float(self.x_end_input.text())
            if self.x_start > self.x_end:
                self.show_error("Начальное значение отображения должно быть больше конечного")
            self.poisson_slider.setMaximum(int(self.x_end + 2))
            self.update_plot()
        except ValueError:
            self.show_error("Невалидное значение для конечного отображения X")


    def update_plot(self):
        self.plot_widget_pmf.clear()
        self.plot_widget_cdf.clear()

        x = np.arange(self.x_start, self.x_end, 1)
        poisson_pmf = poisson.pmf(x, self.poisson_lambda)
        poisson_cdf = poisson.cdf(x, self.poisson_lambda)

        self.plot_widget_pmf.plot(x, poisson_pmf, pen='r', symbol='o', name='PMF Poisson Distribution')
        self.plot_widget_cdf.plot(x, poisson_cdf, pen='b', name='CDF Poisson Distribution')

    def open_uniform_window(self):
        self.uniform_window = UniformDistributionWindow()
        self.uniform_window.show()
        self.close()


def main():
    app = QApplication(sys.argv)
    window = UniformDistributionWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()