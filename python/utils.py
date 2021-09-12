from sympy import lambdify, symbols  # type: ignore
import numpy as np  # type: ignore
from matplotlib.pyplot import figure  # type:ignore
from typing import Any, Tuple


def process_result(result_value: float, result_array: Tuple[float, float], *variable_symbols: symbols):
    """

    Processing result into string to display

    :param result_value:    float
                            min value evaluated by steepest-descent method
    :param result_array:    (float, float)
                            x* and y* so f(x*, y*) = "result_value"
    :param variable_symbols:    symbols
                                symbolic representation of variables

    :return: str: processed string

    """
    processed_string = "f(x*, y*) = " + str("{:.5f}".format(result_value)) + "; "
    for variable_symbol, result_token in zip(variable_symbols, result_array):
        processed_string += str(variable_symbol) + "* = " + str("{:.5f}".format(result_token)) + "; "
    return processed_string


def draw_plot(fig: figure, function: Any, steps: list, *variable_symbols: symbols):
    """

    Drawing steps plot

    :param fig: figure
                The figure to draw plot
    :param function:    Any
                        Sympy parsed function
    :param steps:   list
                    Steepest descent method steps
    :param variable_symbols:    symbols
                                symbolic representation of variables

    """
    fig.clear()
    x, y = variable_symbols
    ax = fig.add_subplot(1, 1, 1)
    ax.grid()

    function_lambda = lambdify((x, y), function, "numpy")
    offset_percent = 5
    # Пока на точке (0, 1) не работает правильное отображние мешгрида
    x_min = min(steps, key=lambda step: step[0])[0] / 100 * (100 + offset_percent)
    x_max = max(steps, key=lambda step: step[0])[0] / 100 * (100 + offset_percent)
    y_min = min(steps, key=lambda step: step[1])[1] / 100 * (100 + offset_percent)
    y_max = max(steps, key=lambda step: step[1])[1] / 100 * (100 + offset_percent)

    print(x_min)

    x_linspace = np.linspace(x_min, x_max, 1000)  # no idea why pycharm can't find np.linspace
    y_linspace = np.linspace(y_min, y_max, 1000)  # no idea why pycharm can't find np.linspace
    x, y = np.meshgrid(x_linspace, y_linspace)
    contour = ax.contourf(x, y, function_lambda(x, y), levels=25)

    for i in range(len(steps) - 1):
        ax.plot((steps[i][0], steps[i + 1][0]), (steps[i][1], steps[i + 1][1]), marker="o", ms=3,
                linewidth=2, color="#ea3c53", label=i)
        ax.annotate(str(i), (steps[i][0], steps[i][1]), color="magenta", fontsize=12, fontweight="demibold")
    ax.annotate(str(len(steps) - 1), (steps[-1][0], steps[-1][1]), color="magenta", fontsize=12,
                fontweight="demibold")

    color_bar = fig.colorbar(contour)
    ax.set_xlabel("x", rotation="horizontal", loc="right")
    ax.set_ylabel("y", rotation="horizontal", loc="top")
    color_bar.set_label("F(x,y)", rotation="horizontal", loc="bottom")
