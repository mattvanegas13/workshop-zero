from __future__ import annotations
from inspect import Parameter
import math
import random
from typing import Any
class Value:
    def __init__(self, data:float, _children= tuple(), _op="", label="") -> None:
        self.data = data
        self.grad = 0.0
        self._backward = lambda : None 
        self._prev = set(_children)
        self._op = _op
        self.label = label
        
    
    def __repr__(self) -> str:
        return f"Value(data={self.data})"
   
    
    def __add__(self, other: Value) -> Value:
        # for convenience so we can add not just values 
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), "+")
        def _backward():
            self.grad += 1.0 * out.grad
            other.grad += 1.0 * out.grad
        out._backward= _backward
        return out
    
    def __radd__(self, other):
        return self + other
    def __rmul__(self, other) ->Value: # in the case where need to do 2 * value -> it will try to do 2 * a but wont know how - so we look at a to find the value of 2*a
        return self * other

    def __mul__(self, other) -> Value:
        other = other if isinstance(other, Value) else Value(other)
        out= Value(self.data * other.data, (self, other), "*")
        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out
   
    
    def __pow__(self, other):
        assert isinstance(other, (int, float))
        out = Value(self.data**other, (self, ), f'**{other}')
        def _backward():
            self.grad += other * (self.data**(other -1 )) * out.grad
            
        out._backward = _backward
        return out 
   
    def __truediv__(self, other ):
        return self * other**-1

    def __neg__(self):
        return self * -1 

    def __sub__(self, other):
        return self + (-other)

    def exp(self):
        x = self.data
        t = math.exp(x)
        out = Value(t, (self, ), 'exp')
        def _backward():
            self.grad += out.data * out.grad # t = out.data -> d/dx [e^x] = e^x
        out._backward = _backward
        return out 
    
    def tanh(self):
        x = self.data
        t = (math.exp(2*x) -1)/ (math.exp(2*x) + 1)
        out= Value(t, (self,), 'tanh')
        def _backward():
            self.grad += (1-t**2) * out.grad
        out._backward = _backward
        return out 
    
    def backward(self):
        topo = []
        visited = set()
        def build_topo(v):
            if not v in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
                
        build_topo(self)
        self.grad = 1.0 # base case
        for node in reversed(topo):
            node._backward()  
            
            
class Neuron:
    def __init__(self, nin: int) -> None:
        self.w = [Value(random.uniform(-1,1)) for _ in range(nin)]
        self.b = Value(random.uniform(-1,1))
        
    def __call__(self, x):
        act = sum((wi*xi for wi,xi in zip(self.w, x)), self.b)
        out = act.tanh()
        return out
    
    def parameters(self):
        # the weights and biases of the neuron
        return self.w + [self.b]
       
       
class Layer:
    def __init__(self, nin, nout) -> None:
        self.neurons = [Neuron(nin) for _ in range(nout)]
        
    def __call__(self, x):
        outs = [n(x) for n in self.neurons]
        return outs[0] if len(outs) == 1 else outs
    
    def parameters(self):
        return [ p for neuron in self.neurons for p in neuron.parameters()]
            
    
class MLP:
    def __init__(self, nin, nouts) -> None:
        sz = [nin] + nouts
        self.layers = [Layer(sz[i], sz[i+1]) for i in range(len(nouts))]
        
    def __call__(self,x):
        for layer in self.layers:
            x = layer(x)
        return x
    
    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]