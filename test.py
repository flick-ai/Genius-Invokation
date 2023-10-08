from enum import Enum

class A(Enum):
    AA = 1
    AB = 2

b = A.AA
c = A(1)

print(A.AA == b)
print(A.AA == c)
print(b == c)

print(A(1) == 1)

print(A.AA is b)
print(A.AA is c)
print(b is c)