from functools import wraps
from typing import Optional, Any, Callable

from simple_profile.types import MemoryUnit, TimeUnit
from simple_profile.utils import measure_peak_memory_usage, measure_average_execution_time, get_function_call_log


def wraps_top_level(function: Callable):
    """
    Runs a function wrapper only if it is a top level function call.
    :param function: the wrapped function
    :return: the decorated wrapper
    """
    def decorator(wrapped: Callable):
        top_level = True

        @wraps(wrapped)
        def wrapper(*args: Any, **kwargs: Any):
            nonlocal top_level

            if top_level:
                try:
                    top_level = False
                    return wrapped(*args, **kwargs)
                finally:
                    top_level = True
            return function(*args, **kwargs)
        return wrapper

    return decorator


def memory_profile(
    name: Optional[str] = None,
    print_args=False,
    print_result=False,
    separator=" | ",
    unit: Optional[MemoryUnit] = None,
    precision=4
):
    """
    Logs the peak memory usage of each function call.
    :param name: the name to use in the logs
    :param print_args: whether to log the arguments
    :param print_result: whether to log the result
    :param separator: the separator to use between log values
    :param unit: the memory unit to use
    :param precision: the memory precision to use (in number of significant digits)
    :return: the decorated function
    """

    def decorator(function: Callable):
        @wraps_top_level(function)
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any):
            peak_memory_usage, result = measure_peak_memory_usage(function, args, kwargs)

            message = get_function_call_log(name, function, args, kwargs, result, print_args, print_result, separator)
            message += separator + MemoryUnit.format_value(peak_memory_usage, unit, precision)
            print(message)

            return result

        return wrapper

    return decorator


def time_profile(
    name: Optional[str] = None,
    iterations=1000000,
    print_args=False,
    print_result=False,
    separator=" | ",
    unit: Optional[TimeUnit] = None,
    precision=4,
    enable_gc=False
):
    """
    Logs the average execution time of each function call.
    :param name: the name to use in the logs
    :param iterations: the number of times to execute the function call
    :param print_args: whether to log the arguments
    :param print_result: whether to log the result
    :param separator: the separator to use between log values
    :param unit: the time unit to use
    :param precision: the time precision to use (in number of significant digits)
    :param enable_gc: whether to enable garbage collection during the measurement
    :return: the decorated function
    """

    def decorator(function: Callable):
        @wraps_top_level(function)
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any):
            average_execution_time = measure_average_execution_time(function, args, kwargs, iterations, enable_gc)
            result = function(*args, **kwargs)

            message = get_function_call_log(name, function, args, kwargs, result, print_args, print_result, separator)
            message += separator + TimeUnit.format_value(average_execution_time, unit, precision)
            print(message)

            return result

        return wrapper

    return decorator


def profile(
    name: Optional[str] = None,
    iterations=1000000,
    print_args=False,
    print_result=False,
    separator=" | ",
    memory_unit: Optional[MemoryUnit] = None,
    memory_precision=4,
    time_unit: Optional[TimeUnit] = None,
    time_precision=4,
    precision: Optional[int] = None,
    enable_gc=False
):
    """
    Logs the peak memory usage and the average execution time of each function call.
    :param name: the name to use in the logs
    :param iterations: the number of times to execute the function call
    :param print_args: whether to log the arguments
    :param print_result: whether to log the result
    :param separator: the separator to use between log values
    :param memory_unit: the memory unit to use
    :param memory_precision: the memory precision to use (in number of significant digits)
    :param time_unit: the time unit to use
    :param time_precision: the time precision to use (in number of significant digits)
    :param precision: the precision to use for all values (in number of significant digits)
    :param enable_gc: whether to enable garbage collection during the measurement
    :return: the decorated function
    """
    if precision is not None:
        memory_precision = precision
        time_precision = precision

    def decorator(function: Callable):
        @wraps_top_level(function)
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any):
            peak_memory_usage, result = measure_peak_memory_usage(function, args, kwargs)
            average_execution_time = measure_average_execution_time(function, args, kwargs, iterations, enable_gc)

            message = get_function_call_log(name, function, args, kwargs, result, print_args, print_result, separator)
            message += separator + MemoryUnit.format_value(peak_memory_usage, memory_unit, memory_precision)
            message += separator + TimeUnit.format_value(average_execution_time, time_unit, time_precision)
            print(message)

            return result

        return wrapper

    return decorator
