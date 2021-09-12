from sympy import diff, symbols  # type: ignore
import numpy as np
from typing import Any, Tuple
from numpy.typing import ArrayLike

golden_ratio = (1 + 5 ** 0.5) / 2


def golden_ratio_input_function(function: Any, variable_symbols: symbols, variable_values: Tuple[float, float],
                                step: float) -> float:
    """

    golden-ratio argument function evaluation

    :param function:    Any
                        Sympy parsed function
    :param variable_symbols:    symbols
                                variable symbolic representation
    :param variable_values: (float, float)
                            variable values in the same order as "variable_symbols"
    :param step:    float
                    golden_ratio step
    :return:    float:
                golden-ratio function result

    """
    function_args = np.zeros(2)

    gradient_value: float
    for i, (variable_value, gradient_value) in enumerate(
            zip(variable_values, get_gradient(function, variable_symbols, variable_values))):
        function_args[i] = variable_value - step * gradient_value
    result = function
    for i, (variable_symbol, function_arg) in enumerate(zip(variable_symbols, function_args)):
        result = result.subs(variable_symbol, function_arg)
    return float(result)


def get_gradient(function: Any, variable_symbols: symbols, variable_values: Tuple[float, float]) -> ArrayLike:
    """

    Gradient vector evaluation

    :param function:    Any
                        Sympy parsed function
    :param variable_symbols:    symbols
                                variable symbolic representation
    :param variable_values: (float, float)
                            variable values in the same order as "variable_symbols"
    :return: list: gradient vector

    """
    gradient = list()
    for i, variable_symbol in enumerate(variable_symbols):
        gradient.append(diff(function, variable_symbol))
    for i in range(len(gradient)):
        for variable_symbol, variable_value in zip(variable_symbols, variable_values):
            gradient[i] = gradient[i].subs(variable_symbol, variable_value)
    gradient = np.array([i for i in map(lambda gradient_token: float(gradient_token), gradient)])
    return gradient


def steepest_descent_method(function: Any, variable_symbols: symbols, start_value: Tuple[float, float],
                            tolerance: float, max_iterations: int = 1000):
    """

    Steepest descent method implementation

    :param function:    Any
                        Sympy parsed function
    :param variable_symbols:    symbols
                                variable symbolic representation
    :param start_value: (float, float)
                        start point
    :param tolerance:   float
                        evaluation tolerance
    :param max_iterations:  int
                            max amount of method iterations

    :return:    list:  Steepest descent method steps

    """
    x_previous = start_value
    steps = [x_previous]
    count = 0
    while True:
        if count > max_iterations:  # flag of possible method divergence
            return []
        count += 1
        step_size = golden_ratio_method(function, variable_symbols, x_previous)
        x_next = x_previous - step_size * get_gradient(function, variable_symbols, x_previous)
        steps.append(x_next)
        if np.linalg.norm(x_next - x_previous) < tolerance:
            break
        x_previous = x_next
    return steps


def golden_ratio_method(function: Any, variable_symbols: symbols, variable_values: Tuple[float, float],
                        tolerance: float = 1e-3) -> float:
    """

    Golden-ratio implementation

    :param function:    Any
                        Sympy parsed function
    :param variable_symbols:    symbols
                                variable symbolic representation
    :param variable_values: (float, float)
                            variable values in the same order as "variable_symbols"
    :param tolerance:   float
                        evaluation tolerance

    :return:    min value evaluated with golden-ratio method

    """
    r_border, l_border = 0.0, 1.0
    while np.abs(r_border - l_border) > tolerance:
        x_1 = r_border - (r_border - l_border) / golden_ratio
        x_2 = l_border + (r_border - l_border) / golden_ratio
        y_1 = golden_ratio_input_function(function, variable_symbols, variable_values, x_1)
        y_2 = golden_ratio_input_function(function, variable_symbols, variable_values, x_2)
        if y_1 >= y_2:
            l_border = x_1
        else:
            r_border = x_2
    return (l_border + r_border) / 2
