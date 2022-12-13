from enum import Enum


class MemoryUnit(Enum):
    BITS = (0.125, "b")
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
