from sympy import symbols  # type:ignore
from PyQt5 import QtCore  # type: ignore
from python.main_window import MainWindow  # type:ignore
from python.utils import process_result  # type:ignore
from python.enums import Error  # type:ignore


def init_test_app(function: str, x_0: str, y_0: str) -> MainWindow:
    """

    Test app initialization

    :param function:    str
                        string representation of function
    :param x_0: str
                string representation of x_0
    :param y_0: str
                string representation of y_0

    :return:    MainWindow: test app

    """
    test_app = MainWindow()
    test_app.line_edit_function.setText(function)
    test_app.line_edit_x_0.setText(x_0)
    test_app.line_edit_y_0.setText(y_0)
    return test_app


def test_correct_input(qtbot):
    """

    Test function for correct input

    """
    test_app = init_test_app("x^2+y^2", "1", "1")
    qtbot.addWidget(test_app)  # qtbot shall be repeated in every test function as it handles single app session
    qtbot.mouseClick(test_app.button_calculate, QtCore.Qt.LeftButton)
    assert test_app.label_result.text() == process_result(0, (0, 0), *symbols("x y"))


def test_forbidden_operation(qtbot):
    """

    Test function for forbidden operations (like x/0 or arcsin(2))

    """
    test_app = init_test_app("x/y", "1", "0")
    qtbot.addWidget(test_app)
    qtbot.mouseClick(test_app.button_calculate, QtCore.Qt.LeftButton)
    assert test_app.label_result.text() == Error.ERROR_FORBIDDEN_OPERATION


def test_divergence(qtbot):
    """

    Test function for divergent function

    """
    test_app = init_test_app("x^2 + y", "1", "1")
    qtbot.addWidget(test_app)
    qtbot.mouseClick(test_app.button_calculate, QtCore.Qt.LeftButton)
    assert test_app.label_result.text() == Error.ERROR_DIVERGENCE


def test_missing_args(qtbot):
    """

    Test function for wrong set of arguments

    """
    test_app = init_test_app("x^2 + z^2", "1", "1")
    qtbot.addWidget(test_app)
    qtbot.mouseClick(test_app.button_calculate, QtCore.Qt.LeftButton)
    assert test_app.label_result.text() == Error.ERROR_MISSING_ARGUMENTS


def test_incorrect_function(qtbot):
    """

    Test function for wrong function input

    """
    test_app = init_test_app("+", "1", "1")
    qtbot.addWidget(test_app)
    qtbot.mouseClick(test_app.button_calculate, QtCore.Qt.LeftButton)
    assert test_app.label_result.text() == Error.ERROR_INCORRECT_FUNCTION


def test_incorrect_dimension(qtbot):
    """

    Test function for wrong function dimension

    """
    test_app = init_test_app("x^2 + 2^8", "1", "1")
    qtbot.addWidget(test_app)
    qtbot.mouseClick(test_app.button_calculate, QtCore.Qt.LeftButton)
    assert test_app.label_result.text() == Error.ERROR_INCORRECT_DIMENSION


def test_incorrect_start(qtbot):
    """

    Test function for incorrect start input

    """
    test_app = init_test_app("x^2 + y^2", "1", "a")
    qtbot.addWidget(test_app)
    qtbot.mouseClick(test_app.button_calculate, QtCore.Qt.LeftButton)
    assert test_app.label_result.text() == Error.ERROR_INCORRECT_START


def test_incorrect_tolerance(qtbot):
    """

    Test function for incorrect tolerance input

    """
    test_app = init_test_app("x^2 + y^2", "1", "a")
    test_app.line_edit_tol.setText("aaa")
    qtbot.addWidget(test_app)
    qtbot.mouseClick(test_app.button_calculate, QtCore.Qt.LeftButton)
    assert test_app.label_result.text() == Error.ERROR_INCORRECT_TOLERANCE
