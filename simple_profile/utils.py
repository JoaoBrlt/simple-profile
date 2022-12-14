import timeit
import tracemalloc
from typing import Any, Callable, Optional


def measure_memory_usage(
    function: Callable,
    args: tuple[Any, ...],
    kwargs: dict[str, Any]
) -> tuple[tuple[int, int], Any]:
    """
    Measures the memory usage of a function call.
    :param function: the function to analyze
    :param args: the arguments to use
    :param kwargs: the keyword arguments to use
    :return: the memory usage of the function call (in bytes) and its result
    """
    tracemalloc.start()
    result = function(*args, **kwargs)
    memory_usage = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return memory_usage, result


def measure_peak_memory_usage(function: Callable, args: tuple[Any, ...], kwargs: dict[str, Any]) -> tuple[int, Any]:
    """
    Measures the peak memory usage of a function call.
    :param function: the function to analyze
    :param args: the arguments to use
    :param kwargs: the keyword arguments to use
    :return: the peak memory usage of the function call (in bytes) and its result
    """
    memory_usage, result = measure_memory_usage(function, args, kwargs)
    return memory_usage[1], result


def measure_execution_time(
    function: Callable,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    iterations: int,
    enable_gc: bool
) -> float:
    """
    Measures the execution time of a function call.
    :param function: the function to analyze
    :param args: the arguments to use
    :param kwargs: the keyword arguments to use
    :param iterations: the number of times to execute the function call
    :param enable_gc: whether to enable garbage collection during the measurement
    :return: the execution time of all the iterations of the function call (in seconds)
    """
    setup = "pass"
    if enable_gc:
        setup = "gc.enable()"
    return timeit.timeit(stmt=lambda: function(*args, **kwargs), setup=setup, number=iterations)


def measure_average_execution_time(
    function: Callable,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    iterations: int,
    enable_gc: bool
) -> float:
    """
    Measures the average execution time of a function call.
    :param function: the function to analyze
    :param iterations: the number of times to execute the function call
    :param args: the arguments to use
    :param kwargs: the keyword arguments to use
    :param enable_gc: whether to enable garbage collection during the measurement
    :return: the average execution time of the function call (in seconds)
    """
    execution_time = measure_execution_time(function, args, kwargs, iterations, enable_gc)
    return execution_time / iterations


def format_array(array: list, separator=", ") -> str:
    """
    Formats an array.
    :param array: the array to format
    :param separator: the separator to use
    :return: the formatted array
    """
    return separator.join([str(item) for item in array])


def format_dict(dictionary: dict, separator=", ") -> str:
    """
    Formats a dictionary.
    :param dictionary: the dictionary to format
    :param separator: the separator to use
    :return: the formatted dictionary
    """
    return separator.join("{}={}".format(key, value) for key, value in dictionary.items())


def format_args(args: tuple[Any, ...], kwargs: dict[str, Any], separator=", ") -> str:
    """
    Formats the arguments of a function
    :param args: the arguments of the function
    :param kwargs: the keyword arguments of the function
    :param separator: the separator to use
    :return: the formatted arguments
    """
    if len(args) > 0 or len(kwargs) > 0:
        return separator.join(
            filter(None, [
                format_array(list(args)),
                format_dict(kwargs)
            ])
        )
    return "None"


def select_profile_name(name: Optional[str], function: Callable) -> str:
    """
    Selects the profile name.
    :param name: the profile name (if provided)
    :param function: the analyzed function
    :return: the profile name
    """
    if name is not None:
        return name
    return function.__name__


def get_function_call_log(
    name: Optional[str],
    function: Callable,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    result: Any,
    print_args: bool,
    print_result: bool,
    separator: str,
) -> str:
    """
    Returns the logging message of a function call.
    :param name: the profile name (if provided)
    :param function: the analyzed function
    :param args: the arguments of the function
    :param kwargs: the keyword arguments of the function
    :param result: the result of the function
    :param print_args: whether to log the function arguments
    :param print_result: whether to log the function result
    :param separator: the separator to use between log values
    :return: the logging message of the function call
    """
    message = select_profile_name(name, function)
    if print_args:
        message += separator + format_args(args, kwargs)
    if print_result:
        message += separator + str(result)
    return message
