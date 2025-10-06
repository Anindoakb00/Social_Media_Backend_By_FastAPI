import pytest
from app.calculations import add


def test_add():
  print('testing add funtion')
  assert add(5,3) == 8

  