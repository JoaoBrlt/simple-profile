from enum import Enum
from typing import Type, TypeVar, Optional, cast

E = TypeVar("E", bound="ExtendedEnum")
U = TypeVar("U", bound="Unit")


class ExtendedEnum(Enum):

    @classmethod
    def list(cls: Type[E]) -> list[E]:
        """
        Returns the list of enumerated values.
        :return: the list of enumerated values
        """
        return list(map(lambda item: item, cls))


class Unit(ExtendedEnum):

    def scale(self) -> float:
        """
        Returns the scale of the unit.
        This value corresponds to a number of units in relation to the standard unit (scale = 1).
        :return: the scale of the unit
        """
        return float(self.value[0])

    def label(self) -> str:
        """
        Returns the label of the unit.
        :return: the label of the unit
        """
        return str(self.value[1])

    def selectable(self) -> bool:
        """
        Indicates whether a unit can be automatically selected.
        :return: True if the unit can be automatically selected; False otherwise.
        """
        return len(cast(tuple, self.value)) < 3 or bool(self.value[2])

    @classmethod
    def select_by_value(cls: Type[U], value: float) -> U:
        """
        Selects the most suitable unit for a value.
        :param value: the value to analyze
        :return: the most suitable unit for the provided value
        """
        units = cls.list()
        units.sort(key=lambda item: item.scale(), reverse=True)
        for unit in units:
            if unit.selectable() and value >= unit.scale():
                return unit
        return units[-1]

    @classmethod
    def format_value(cls: Type[U], value: float, unit: Optional[U], precision: int) -> str:
        """
        Formats a value.
        If no unit is provided, it is automatically selected depending on the value to format.
        :param value: the value to format
        :param unit: the unit to use
        :param precision: the precision to use (in number of significant digits)
        :return: the formatted value
        """
        if unit is None:
            unit = cls.select_by_value(value)
        return "{value:.{precision}g} {unit}".format(
            value=value / unit.scale(),
            unit=unit.label(),
            precision=precision
        )


class MemoryUnit(Unit):
    BITS = (0.125, "b")
    BYTES = (1, "B")
    KILOBYTES = (1E3, "kB")
    KIBIBYTES = (1024, "kiB", False)
    MEGABYTES = (1E6, "MB")
    MEBIBYTES = (1048576, "MiB", False)
    GIGABYTES = (1E9, "GB")
    GIBIBYTES = (1073741824, "GiB", False)
    TERABYTES = (1E12, "TB")
    TEBIBYTES = (1099511627776, "TiB", False)


class TimeUnit(Unit):
    NANOSECONDS = (1E-9, "ns")
    MICROSECONDS = (1E-6, "µs")
    MILLISECONDS = (1E-3, "ms")
    SECONDS = (1, "s")
    MINUTES = (60, "m")
    HOURS = (3600, "h")
    DAYS = (86400, "d")
