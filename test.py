from nis import match
from unittest import case


i = [-4.43132432, 0, 34.4523, -2.3445]
y = sorted(i)
print(i)

def func(ar):
    match ar:
        case 0:
            return 1