
from icecream import ic
ic.configureOutput(includeContext=False)

name = "Alice"
age = 30
ic(name, age)

def foo(i):
    return i + 333

ic(foo(123))