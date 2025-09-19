from abc import ABC, abstractmethod

import module
module.some()

from module import some as some2
some2()

def decorator_with_args(fn):
    def wrapped(arg):
        return "<b>" + fn(arg) + "</b>"
    return wrapped  
@decorator_with_args
def hello(arg):
    return ("Hello, World!") * arg
print(hello(3))

def outer(fn):
    def inner(*args, **kwargs):
        print("Before function call")
        result = fn(*args, **kwargs)
        print("After function call")
        return result
    return inner
@outer
def greet(name):
    return f"Hello, {name}!"
print(greet("Alice"))

def outer2(a):
    def decorator(fn):
        def inner(*args, **kwargs):
            print(f"Decorator argument: {a}")
            return fn(*args, **kwargs)
        return inner
    return decorator  
@outer2("example")
def greet2(name):
    return f"Hello, {name}!"
print(greet2("Bob"))


b = b'Hello'                   # литерал ('bytes literal') ёл-си
print(b[0])
b = bytes([72, 101, 108, 108, 111])  # конструктор
print(f"b: 0x{b[0]:X}")         
b = bytearray(b'Hello')        # конструктор, возвращает изменяемый
b = bytes.fromhex('48656c6c6f')  # конструктор, возвращает неизменяемый 
b = b'Hello, World!'           # байтовая строка
print(b)                       # вывод: b'Hello, World!'
print(type(b))

some = True
result = 1 if some else 0

class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass

class Cat(Animal):
    def make_sound(self):
        print("Meow!")
    
    
c = Cat()    

def f(arg: list = []):
    arg.append(1)
    # print(arg)
    return arg

bb = 2
def some(a: int) -> int:
    global bb
    print(f"bb: {bb}")
    bb = 3
    print(locals())
    return a + 1  

class Person:
    name: str
    public: str = "public"
    _protected: str = "protected"
    __private: str = "private"

    def __init__(self, name: str):
        self.name = name
    
    @property
    def newName(self):
        return self.name
    
    @newName.setter
    def newName(self, value: str):
        self.name = value

    def say_hello(self):
        print(f"Hello, my name is {self.name}!")  
    
    @classmethod
    def from_string(cls, name: str):
        return cls(name)
    
    @staticmethod
    def static_method():
        print("This is a static method.")

Person.static_method()         

Person.from_string("Bob").say_hello()

p = Person("Alice")
print(Person.__dict__)
print("-----------")
print(dir(p))

p.say_hello()

print("-----------")
print(p.newName)
p.newName = "New Name"
print(p.newName)
print(p.name)



if __name__ == "__main__":
    print("This script is being run directly.")
else:
    print("This script is being imported as a module.")

some(3)
print(f"[2]bb: {bb}")


import copy
a = [1, [2]]
b = [4, 5, 6,7]
c = [8,9]
for i in zip(a, b, c):
    print(i)
print(type(i))

a = [i for i in range(10)]
b = filter(lambda x: x % 2 == 0, a)
print(a)
print(list(b))

b = copy.deepcopy(a)
b.append(3)
b[1].append(4)
print(a)
print(b)

b = list(a)
b = a[:]
b = a.copy()
b =  [i for i in a]
print(a)
print(b)

l = [i for i in range(10)]
print(l)

s = (i for i in range(10))
print(s)
print(type(s))
print(next(s))
print(next(s))
print(next(s))

s = {i: i*2 for i in range(10)}
print(s)
print(type(s))

nWord = 0
word = ""
result = True
print(f())
print(f())
print(f())

# while True:
#     try:
#         s = input("Введите целое (exit — для выхода): ")
#         if s == "exit":
#             break
#         x = int(s)
#         print("Введён квадрат:", x**2)
#     except ValueError:
#         print("Нужно целое число.")
#     else:
#         print("Введён квадрат:", x**2)
#     finally:
#         print("--- итерация завершена ---")

# def safe_div(a, b):
#     try:
#         return a / b
#     except ZeroDivisionError:
#         return float('inf')

# print(safe_div(10, 0))  # inf


try:
    data = input("Введите число: ")
    n = int(data)
    print("Квадрат", n**2)
# except ValueError:
#     print("Это не валидное целое число.")
except KeyboardInterrupt:
    print("\n Пользователь прервал ввод.")
except Exception as e:
    print("Неожиданная ошибка:", type(e).__name__, str(e))
exit(0)

list_a = [1, 2, 3]
list_b = list_a
print(id(list_a)) # идентификатор списка list_a
print(id(list_b)) # идентификатор списка list_b

print("Enter the number of words:")
nWord = int(input())
for i in range(nWord):
    word = input()
    print("Word:", word)
    print(f"1 {(word.find('a') != 0)} 2 {(word.find('b') != 0)} 3  {(word.find('c') != 0)}") 

    breakpoint()
    
    if (word.find('a') != 0) and (word.find('b') != 0) and (word.find('c')):
        result = False
if (result == True):
    print('YES')
else:
    print('NO')


if __name__ == "__main__":
    print("This script is being run directly.")
else:
    print("This script is being imported as a module.")