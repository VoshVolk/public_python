# contents of test_append.py
import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from sample import first_entry

# @pytest.fixture
# def first_entry():
#     return "a"


@pytest.fixture
def order(first_entry):
    return [first_entry]


@pytest.fixture()
def append_first(order, first_entry):
    for s in range(100000000):
        pass
    print("\n",order)
    return order.append(first_entry)


def test_string_only(order, first_entry):
    print("\n",order)
    assert order == [first_entry]


def test_string_and_int(order, first_entry):
    order.append(2)
    print("\n",order)
    assert order == [first_entry, 2]