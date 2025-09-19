import pytest

@pytest.fixture
def sample_data():
  return {"x": 1, "y": 2}

def test_sum(sample_data):
  assert sample_data["x"] + sample_data["y"] == 3

def test_addition():
  assert 1 + 1 == 2

@pytest.mark.parametrize("a,b,expected", [(1,2,3), (2,3,5), (10,15,25)])
def test_add(a, b, expected):
  assert a + b == expected

@pytest.mark.only_this
@pytest.mark.parametrize("input,expected", [
    ("3+55", 8),
    ("2+4", 6),
    ("6*9", 54),
])
def test_eval(input, expected):
    assert eval(input) == expected
#####################
"""Проверим тип данных Task."""

from collections import namedtuple
Task = namedtuple('Task', ['summary', 'owner', 'done', 'id'])
Task.__new__.__defaults__ = (None, None, False, None)

def test_defaults():
    """Без использования параметров, следует ссылаться на значения по умолчанию."""
    t1 = Task()
    t2 = Task(None, None, False, None)
    assert t1 == t2

def test_member_access():
    """Проверка свойства .field (поля) namedtuple."""
    t = Task('buy milk', 'brian')
    assert t.summary == 'buy milk'
    assert t.owner == 'brian'
    assert (t.done, t.id) == (False, None)

def test_asdict():
    """_asdict() должен возвращать словарь."""
    t_task = Task('do something', 'okken', True, 21)
    t_dict = t_task._asdict()
    expected = {'summary': 'do something',
                'owner': 'okken',
                'done': True,
                'id': 21}
    assert t_dict == expected

def test_replace():
    """должно изменить переданное в fields."""
    t_before = Task('finish book', 'brian', False)
    t_after = t_before._replace(id=10, done=True)
    t_expected = Task('finish book', 'brian', True, 10)
    assert t_after == t_expected    