# simple-profile

[![CI][ci-badge-url]][ci-workflow-url]

Simple decorators to profile the memory usage and execution time.

## Installation

```bash
pip install simple-profile
```

## Decorators

| Decorator           | Description                                                                  |
|---------------------|------------------------------------------------------------------------------|
| `@profile()`        | Profiles the peak memory usage and the average execution time of a function. |
| `@memory_profile()` | Profiles only the peak memory usage of a function.                           |
| `@time_profile()`   | Profiles only the average execution time of a function.                      |

## Usage

### 1. Profile a function

The `@profile()` decorator allows to log the peak memory usage and the average execution time of each function call.\
By default, memory usage and execution time are logged in the most suitable units, but it is possible to change the units.

```python
from simple_profile import profile

@profile()
def my_function():
    return [2 * i for i in range(10)]

my_function()
```

Output: 

```
my_function | 432 B | 445.2 ns
```

### 2. Profile only the memory usage of a function

The `@memory_profile()` decorator allows to log the peak memory usage of each function call.\
This is done using the `tracemalloc` module provided by Python.

```python
from simple_profile import memory_profile

@memory_profile()
def my_function():
    return [2 * i for i in range(10)]

my_function()
```

Output: 

```
my_function | 432 B
```

### 3. Profile only the execution time of a function

The `@time_profile()` decorator allows to log the average execution time of each function call.\
This is done using the `timeit` module provided by Python.\
By default, each function call is repeated `1,000,000` times to get a reliable measurement, but it is possible to change this value.

```python
from simple_profile import time_profile

@time_profile()
def my_function():
    return [2 * i for i in range(10)]

my_function()
```

Output: 

```
my_function | 439.3 ns
```

### 4. Change the number of iterations

It is possible to change the number of times a function call is repeated when profiling the execution time.\
To do this, you can set the `iterations` argument of the `profile()` and `time_profile()` decorators.

```python
from simple_profile import profile

@profile(iterations=100)
def pi(n):
    result = 0
    d = 1
    for i in range(1, n):
        a = 2 * (i % 2) - 1
        result += 4 * a / d
        d += 2
    return result

pi(100)
```

Output:

```
pi | 168 B | 6.461 µs
```

### 5. Change the time and memory units

It is also possible to change the time and memory units used in the logs.\
To do this, you can set the `unit` argument of the `memory_profile()` and `time_profile()` decorators.\
For the `profile()` decorator, you can set the `time_unit` and `memory_unit` arguments.

```python
from simple_profile import profile, MemoryUnit, TimeUnit

@profile(memory_unit=MemoryUnit.KILOBYTES, time_unit=TimeUnit.MILLISECONDS)
def exponential(x, n):
    result = 1.0
    for i in range(n, 0, -1):
        result = 1 + x * result / i
    return result

exponential(8, 100)
```

Output:

```
exponential | 0.168 kB | 0.005429 ms
```

### 6. Change the time and memory precision

Moreover, it is possible to change the precision of memory and time values.\
To do this, you can define the number of significant digits you want in the `precision` argument of any decorator provided by this package.\
For the `profile()` decorator, you can set the `time_precision` and `memory_precision` arguments for more granular control.

```python
from simple_profile import profile

@profile(precision=10)
def average(lst):
    return sum(lst) / len(lst)

average([25, 12, 18, 88, 64, 55, 22])
```

Output:

```
average | 120 B | 176.6314 ns
```

### 7. Log the arguments and the result

Furthermore, it is possible to log the arguments and the result of each function call.\
Indeed, this can be useful to better profile a function and analyze its behavior.

```python
from simple_profile import profile

@profile(print_args=True, print_result=True)
def greeting_message(name, coins):
    return "Hello {}! You have {} coins.".format(name, coins)

greeting_message("John", coins=5)
```

Output:

```
greeting_message | John, coins=5 | Hello John! You have 5 coins. | 521 B | 350.1 ns
```

### 8. Set a custom name for a function

Additionally, it is possible to define a custom descriptive name for each function.\
To do this, you can set the `name` argument of any decorator provided by this package.

```python
from simple_profile import profile

@profile(name="Naive method")
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

factorial(10)
```

Output:

```
Naive method | 160 B | 411.3 ns
```

### 9. Compare multiple functions

```python
from simple_profile import profile

@profile(name="List comprehension")
def my_function(n):
    return [pow(2, i) for i in range(n)]


@profile(name="For loop")
def my_function_2(n):
    lst = []
    for i in range(n):
        lst.append(pow(2, i))
    return lst

my_function(10)
my_function_2(10)
```

Output:

```
List comprehension | 464 B | 666.8 ns
For loop | 312 B | 650.7 ns
```

### 10. Profile a recursive function

The decorators work seamlessly with recursive functions.\
Only one profiling message is logged per function call even if the function is recursive.

```python
from simple_profile import profile

@profile(print_args=True, print_result=True, iterations=100)
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

fibonacci(10)
```

Output:

```
fibonacci | 10 | 55 | 1.648 kB | 21.04 µs
```

### 11. Enable garbage collection during measurements

By default, garbage collection is temporarily turned off to make measurements more comparable, but it is possible to enable it if you prefer.\
To do this, you can set the `enable_gc` argument of the `profile()` and `time_profile()` decorators to `True`.

```python
from simple_profile import profile

@profile(name="Without GC")
def my_function():
    return [oct(i) for i in range(10)]

@profile(name="With GC", enable_gc=True)
def my_function_2():
    return [oct(i) for i in range(10)]

my_function()
my_function_2()
```

Output:

```
Without GC | 954 B | 666.5 ns
With GC | 954 B | 669.2 ns
```

## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details.

[ci-badge-url]: https://github.com/JoaoBrlt/simple-profile/actions/workflows/ci.yml/badge.svg
[ci-workflow-url]: https://github.com/JoaoBrlt/simple-profile/actions/workflows/ci.yml