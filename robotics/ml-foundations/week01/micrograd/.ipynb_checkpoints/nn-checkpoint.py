from __future__ import annotations
from viz import draw_dot
class Value:
    def __init__(self, data:float, _children= tuple(), _op="", label="") -> None:
        self.data = data
        self._prev = set(_children)
        self._op = _op
        self.label = label
    
    def __repr__(self) -> str:
        return f"Value(data={self.data}, children={self._prev})"
    def __add__(self, other: Value) -> Value:
        return Value(self.data + other.data, (self, other), "+")
    def __mul__(self, other: Value) -> Value:
        return Value(self.data * other.data, (self, other), "*")
    
def main():
    v = Value(2.0, label="v")
    f = Value(3.0, label="f")
    c = v + f
    print(c)
    print(c._prev)
    draw_dot(c) 
    
main()