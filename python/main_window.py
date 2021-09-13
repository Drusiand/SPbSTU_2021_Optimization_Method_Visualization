from PyQt5 import uic  # type: ignore
from PyQt5.QtGui import QIcon  # type: ignore
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QLineEdit, QVBoxLayout  # type: ignore

from sympy import symbols  # type: ignore
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application, parse_expr  # type: ignore

import matplotlib.pyplot as plt  # type: ignore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # type: ignore
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar  # type: ignore

from python.enums import Error  # type:ignore
from python.solver import steepest_descent_method  # type: ignore
from python.utils import draw_plot, process_result  # type: ignore

from typing import Any, Tuple, Union

TITLE = "Gradient visualizer"
ICON_PATH = "source/assets/icon.png"
UI_PATH = "source/ui/main_window.ui"

DEFAULT_TOLERANCE = 1e-6


class MainWindow(QMainWindow):
    line_edit_function: QLineEdit
    line_edit_x_0: QLineEdit
    line_edit_y_0: QLineEdit
    line_edit_tol: QLineEdit
    label_plot: QLabel
    label_result: QLabel
    button_calculate: QPushButton
    button_reset: QPushButton
    canvas_plot: FigureCanvas
    navigation_toolbar_plot: NavigationToolbar
    figure: plt.figure
    # QLabel margins modification shall be done in code as QtDesigner uses obsolete way to set margins
    label_info: QLabel
    margin_left, margin_top, margin_bottom, margin_right = 8, 3, 0, 8

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self, path=UI_PATH):
        """

        UI initialization

        :param path:    str
                        path to .ui module

        """
        uic.loadUi(path, self)

        self.setWindowTitle(TITLE)
        self.setWindowIcon(QIcon(ICON_PATH))

        self.button_calculate.clicked.connect(self.button_calculate_action)

        self.button_reset.clicked.connect(self.button_reset_action)
        self.label_info.setContentsMargins(self.margin_left, self.margin_top, self.margin_right, self.margin_bottom)
        self.label_result.setText("")

        self.figure = plt.figure(tight_layout=True, frameon=False)
        self.canvas_plot = FigureCanvas(self.figure)
        self.canvas_plot.setParent(self.label_plot)
        self.navigation_toolbar_plot = NavigationToolbar(self.canvas_plot, self)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas_plot)
        layout.addWidget(self.navigation_toolbar_plot)

        self.label_plot.setLayout(layout)

    def button_reset_action(self):
        """

        Action for pushing "reset" button

        """
        self.line_edit_function.clear()
        self.line_edit_x_0.clear()
        self.line_edit_y_0.clear()
        self.label_result.clear()

        self.figure.clear()
        self.canvas_plot.draw()

    def button_calculate_action(self):
        """

        Action for pushing "calculate" button

        """

        self.label_result.clear()

        function = self.get_input_function()
        x_0, y_0 = self.get_input_start()
        tolerance = self.get_tolerance()

        if function is not None and x_0 is not None and y_0 is not None and tolerance is not None:
            x, y = symbols("x y")
            if x and y in function.free_symbols:
                try:
                    steps = steepest_descent_method(function, (x, y), (x_0, y_0), tolerance)
                except TypeError:
                    self.label_result.setText(Error.ERROR_FORBIDDEN_OPERATION)
                    return
                if len(steps) == 0:
                    self.label_result.setText(Error.ERROR_DIVERGENCE)
                    return
                result_text = process_result(function.subs(x, steps[-1][0]).subs(y, steps[-1][1]), steps[-1], x, y)
                self.label_result.setText(result_text)
                draw_plot(self.figure, function, steps, x, y)
                self.canvas_plot.draw()
            else:
                self.label_result.setText(Error.ERROR_MISSING_ARGUMENTS)

    def get_input_function(self) -> Any:
        """

        Input function grabber

        :return: Any: parsed sympy function

        """
        function_str = self.line_edit_function.text()
        function_str = function_str.replace("^", "**")
        transformations = (standard_transformations + (implicit_multiplication_application,))
        try:
            function = parse_expr(function_str, transformations=transformations)
        except Exception:  # Only way to handle wrong input for some reason
            self.label_result.setText(Error.ERROR_INCORRECT_FUNCTION)
            return None
        else:
            if len(function.free_symbols) != 2:
                self.label_result.setText(Error.ERROR_INCORRECT_DIMENSION)
                return None
            return function

    def get_input_start(self) -> Union[Tuple[float, float], Tuple[None, None]]:
        """

        Input start point grabber

        :return: (float, float): start point

        """
        try:
            x_0, y_0 = float(parse_expr(self.line_edit_x_0.text().replace(",", "."))), float(
                parse_expr(self.line_edit_y_0.text().replace(",", ".")))
        except Exception:  # Only way to handle wrong input for some reason
            self.label_result.setText(Error.ERROR_INCORRECT_START)
            return None, None
        else:
            return x_0, y_0

    def get_tolerance(self) -> Union[float, None]:
        """

        Input tolerance value grabber

        :return: float: evaluation tolerance

        """
        if self.line_edit_tol.text() == "":
            return DEFAULT_TOLERANCE
        try:
            tolerance = float(parse_expr(self.line_edit_tol.text().replace(",", ".")))
        except Exception:  # Only way to handle wrong input for some reason
            self.label_result.setText(Error.ERROR_INCORRECT_TOLERANCE)
            return None
        else:
            return tolerance
