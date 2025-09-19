import pdb
def decorator_with_args(fn):
  def wrapped(arg):
    return "<b>" + fn(arg) + "</b>"
  return wrapped

@decorator_with_args
def hello(arg):
    breakpoint()
    return ("Hello, World!")*arg

print(hello(3))

# breakpoint()
# fn = makebold(hello)
# print(fn()) 

# my_list = [1, 2, 3]
# my_list = (1, 2, 3)
my_list = {1, 2, 3}
my_iterator = iter(my_list)

print(next(my_iterator))  # Вывод: 1
print(next(my_iterator))  # Вывод: 2
print(next(my_iterator))  # Вывод: 3

try:
    print(next(my_iterator))
except StopIteration:
    print("Конец списка") # Вывод: Конец списка