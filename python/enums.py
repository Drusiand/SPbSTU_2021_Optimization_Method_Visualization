from enum import Enum


class Error(str, Enum):
    ERROR_FORBIDDEN_OPERATION = "ERROR: forbidden operation"
    ERROR_DIVERGENCE = "ERROR: too many iterations, method may diverge"
    ERROR_MISSING_ARGUMENTS = "ERROR: some arguments missing"
    ERROR_INCORRECT_FUNCTION = "ERROR: incorrect function input"
    ERROR_INCORRECT_DIMENSION = "ERROR: incorrect function dimension, consider using function of 2 variables"
    ERROR_INCORRECT_START = "ERROR: incorrect start point input"
    ERROR_INCORRECT_TOLERANCE = "ERROR: incorrect tolerance input"
