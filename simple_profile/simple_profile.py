import timeit
import tracemalloc
from enum import Enum
from typing import cast, Any


class MemoryUnit(Enum):
    BYTES = (1, "B")
    KILOBYTES = (10E3, "kB")
    KIBIBYTES = (1024, "kiB")
    MEGABYTES = (10E6, "MB")
    MEBIBYTES = (1048576, "MiB")
    GIGABYTES = (10E9, "GB")
    GIBIBYTES = (1073741824, "GiB")
    TERABYTES = (10E12, "TB")
    TEBIBYTES = (1099511627776, "TiB")


class TimeUnit(Enum):
    NANOSECONDS = (10E-9, "ns")
    MICROSECONDS = (10E-6, "µs")
    MILLISECONDS = (10E-3, "ms")
    SECONDS = (1, "s")
    MINUTES = (60, "m")
    HOURS = (3600, "h")
    DAYS = (86400, "d")


def get_memory_usage(function, *args, **kwargs) -> tuple[tuple[int, int], Any]:
    tracemalloc.start()
    result = function(*args, **kwargs)
    memory_usage = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return memory_usage, result


def get_peak_memory_usage(function, *args, **kwargs) -> tuple[int, Any]:
    memory_usage, result = get_memory_usage(function, *args, **kwargs)
    return memory_usage[1], result


def get_execution_time(function, iterations: int, *args, **kwargs) -> float:
    return timeit.timeit(lambda: function(*args, **kwargs), number=iterations)


def get_average_execution_time(function, iterations: int, *args, **kwargs) -> float:
    execution_time = get_execution_time(function, iterations, *args, **kwargs)
    return execution_time / iterations


def format_profile_name(name: str, function) -> str:
    if name is not None:
        return name
    return function.__name__


def format_memory(value: int, unit: MemoryUnit) -> str:
    formatted_value = value / cast(int, unit.value[0])
    unit_symbol = cast(str, unit.value[1])
    return "{} {}".format(formatted_value, unit_symbol)


def format_time(value: float, unit: TimeUnit) -> str:
    formatted_value = value / cast(float, unit.value[0])
    unit_symbol = cast(str, unit.value[1])
    return "{} {}".format(formatted_value, unit_symbol)


def memory_profile(
    name=None,
    memory_unit: MemoryUnit = MemoryUnit.KILOBYTES
):
    def decorator(function):
        def wrapper(*args, **kwargs):
            peak_memory_usage, result = get_peak_memory_usage(function, *args, **kwargs)

            print(format_profile_name(name, function), end=" | ")
            print(format_memory(peak_memory_usage, memory_unit))

            return result
        return wrapper
    return decorator


def time_profile(
    name: str = None,
    iterations=10000,
    time_unit: TimeUnit = TimeUnit.MICROSECONDS,
):
    def decorator(function):
        def wrapper(*args, **kwargs):
            average_execution_time = get_average_execution_time(function, iterations, *args, **kwargs)

            print(format_profile_name(name, function), end=" | ")
            print(format_time(average_execution_time, time_unit))

            return function(*args, **kwargs)
        return wrapper
    return decorator


def profile(
    name=None,
    iterations=10000,
    time_unit: TimeUnit = TimeUnit.MICROSECONDS,
    memory_unit: MemoryUnit = MemoryUnit.KILOBYTES
):
    def decorator(function):
        def wrapper(*args, **kwargs):
            peak_memory_usage, result = get_peak_memory_usage(function, *args, **kwargs)
            average_execution_time = get_average_execution_time(function, iterations, *args, **kwargs)

            print(format_profile_name(name, function), end=" | ")
            print(format_memory(peak_memory_usage, memory_unit), end=" | ")
            print(format_time(average_execution_time, time_unit))

            return result
        return wrapper
    return decorator
