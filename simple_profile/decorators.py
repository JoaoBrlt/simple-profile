from typing import Optional, Any, Callable

from simple_profile.types import MemoryUnit, TimeUnit
from simple_profile.utils import measure_peak_memory_usage, measure_average_execution_time, get_function_call_log, \
    format_memory_value, format_time_value


def memory_profile(
    name: Optional[str] = None,
    print_args=False,
    print_result=False,
    separator=" | ",
    unit=MemoryUnit.BYTES,
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
        def wrapper(*args: Any, **kwargs: Any):
            peak_memory_usage, result = measure_peak_memory_usage(function, args, kwargs)

            message = get_function_call_log(name, function, args, kwargs, result, print_args, print_result, separator)
            message += separator + format_memory_value(peak_memory_usage, unit, precision)
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
    unit=TimeUnit.NANOSECONDS,
    precision=4
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
    :return: the decorated function
    """
    def decorator(function: Callable):
        def wrapper(*args: Any, **kwargs: Any):
            average_execution_time = measure_average_execution_time(function, args, kwargs, iterations)
            result = function(*args, **kwargs)

            message = get_function_call_log(name, function, args, kwargs, result, print_args, print_result, separator)
            message += separator + format_time_value(average_execution_time, unit, precision)
            print(message)

            return result
        return wrapper
    return decorator


def simple_profile(
    name: Optional[str] = None,
    iterations=1000000,
    print_args=False,
    print_result=False,
    separator=" | ",
    memory_unit=MemoryUnit.BYTES,
    memory_precision=4,
    time_unit=TimeUnit.NANOSECONDS,
    time_precision=4,
    precision=None
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
    :return: the decorated function
    """
    def decorator(function: Callable):
        def wrapper(*args: Any, **kwargs: Any):
            peak_memory_usage, result = measure_peak_memory_usage(function, args, kwargs)
            average_execution_time = measure_average_execution_time(function, args, kwargs, iterations)

            actual_memory_precision = memory_precision
            actual_time_precision = time_precision
            if precision is not None:
                actual_memory_precision = precision
                actual_time_precision = precision

            message = get_function_call_log(name, function, args, kwargs, result, print_args, print_result, separator)
            message += separator + format_memory_value(peak_memory_usage, memory_unit, actual_memory_precision)
            message += separator + format_time_value(average_execution_time, time_unit, actual_time_precision)
            print(message)

            return result
        return wrapper
    return decorator
