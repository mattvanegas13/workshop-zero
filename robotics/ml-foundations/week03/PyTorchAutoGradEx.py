import torch 
from typing import List, NamedTuple, Callable, Dict, Optional

_name: int = 0
def fresh_name() -> str:
    " create a unique name for a variable: v0, v1 ..."
    global _name
    r = f'v{_name}'
    _name +=1 
    return r

class Variable:
    """ 
    Remember our Value() class from karpathy's tutorial
    this is how we defined our constructor - since we're
    using pytorch. We can reduce the complexity
    """
    
    
    """
    def __init__(self, data, grad, op, prevChildren=tuple()):
        self.data = data
        self.grad = 0.0
        self._backward = lambda : None 
        self._prev = set(_children)
        self._op = _op
        self.label = label
    """
    
    def __init__(self, value:torch.Tensor, name:str="") -> None:
        self.value = value # the tensor
        self.name = name or fresh_name()
    
    # We need to start with leaf nodes before we can build a tree 
    # so lets define a method that we can use to instantiate other leaf nodes
    @staticmethod
    def constant(value:torch.Tensor, name:str=""):
        r = Variable(value=value, name=name)
        print(f'{r.name} = {value}')
        return r
        
    def __repr__(self):
        return repr(self.value)
    
    # This performs a pointwise multiplication of a Variable, tracking gradients
    def __mul__(self, rhs: 'Variable') -> 'Variable':
        # defined later in the notebook
        if isinstance(rhs, float) and rhs==1.0:
            # peephole optimization - this doesn't do anything computationally
            return self
        

        '''
        the equivalent of our _backwards in that case we would compute it in mathematically with the chain rule which resulted in something like below
        
        recall previously
        o = tanh(n)
        n = x1w1 + x2x2 + b
        and if we want to do/dx2 
        
        # x2*w2 = x2 * w2
        # do/dx2 = do/dn * dn/d{x1w1+x2w2) * d{x1w1+x2w2}/dx2w2 * dx2w2 / dx2 = [ do/dx2w2 ] * dx2w2/dx2
        where do/dx2w2 the encompassing  term for all the partials walking up the chain
        - its its local gradient * the upstream aggregation of the other partial chains along the DAG path until there
          we can generalize this in the _backward function for mult
        self.grad += rhs.data(the gradient of all who came before) * r.grad (the local gradient)
        rhs.grad += self.data * r.grad (with this approach we must know how much the nudge on other Value object has an effect on the output)
        
        this tutorial suggest an alternative approach called backwards autodiff
        lets simplify this further and define this expression:
        
        d = a * c 
        where c = a + b
        Here we answer the same question similarly... well to an extent anyways
        
        because we don't have an explicit accumulatory bucket for the gradient, the idea is to chain the appropriate gradient calculations for our gradient tape - 
        
        well what does that mean?
        meaning the tape of that exists from the rhs node and the current node where we are at must be collected and passed up - which is why we define the following
        propogation function 
        '''
        r = Variable(self.value * rhs.value)
        print(f'{r.name} = {self.name} * {rhs.name}')
        # what goes into this node is 
        inputs = [self.name, rhs.name]
        outputs = [r.name] # the new node

        # in this case d = a * c => r = self * rhs 
        def propagate(dL_doutputs: List[Variable]): 
            dL_dr, = dL_doutputs # the gradient chain until our new variable r 
            # now we compute the local gradients
            dr_dself = rhs # dr/dself = d/dself[self *rhs] => rhs 
            dr_drhs = self # similarly
            dL_dself = dL_dr * dr_dself # calculating the gradient of the loss with respect to the current value
            dL_drhs = dL_dr * dr_drhs # calulating the gradient of the loss  with respect to what whever is coming in from the sub ter
            dL_dinputs = [dL_dself, dL_drhs] # collection of the gradients
            return dL_dinputs
        # finally, we record the compute we did on the tape
        gradient_tape.append(TapeEntry(inputs=inputs, outputs=outputs, propagate=propagate)) 
        return r
            

    def __add__(self, rhs: 'Variable') -> 'Variable':
        if isinstance(rhs, float) and rhs==0:
            return self
        
        r = Variable(self.value + rhs.value)
        print(f'{r.name} = {self.name} + {rhs.name}')
        inputs = [self.name, rhs.name]
        outputs = [r.name]
        def propagate(dL_doutputs:List[Variable]):
            # Similarly now we have d = a + c = self + rhs
            dL_dr, = dL_doutputs
            dr_dself = 1.0
            dr_drhs = 1.0
            dL_dself = dL_dr * dr_dself
            dL_drhs = dL_dr *dr_drhs
            return [dL_dself, dL_drhs]
        gradient_tape.append(TapeEntry(inputs=inputs, outputs=outputs, propagate=propagate))
        return r
            
            
    """
    So these are not traditional operations in the sense of the above two
    but they are operationst that can be placed in a DAG - in which they 
    can transform values - as a result of this they need backwards rules
    
    similar to our derivation -> in this case the propogation is how to undo their transforms
    
    technically we can also view the above two operations in the same way *** [this seems like a p big concept]
    a, y -> d 
    thus the backwards transform
    dL/dr -> dL/da, dL/dy
    """
    
    def sum(self, name: Optional[str]=None) -> 'Variable':
        # sum is used on turn our tensors into a single scalar to get a loss 
        r = Variable(torch.sum(self.value), name=name)
        print(f'{r.name} = {self.name}.sum()')
 
        def propagate(dL_doutputs:List[Variable]):
            dL_dr, = dL_doutputs # this is to fetch the last element (i.e itself)
            size = self.value.size()
            return [dL_dr.expand(*size)] # returns tensor whose shape is equal to len(size)? 
        gradient_tape.append(TapeEntry(inputs=[self.name], outputs=[r.name], propagate=propagate))
        return r
        
    def expand(self, sizes: List[int]) -> 'Variable':
        # the opposite of sum - take a scalar and return a tensor 
        assert (self.value.dim() ==0) # should only take scalars
        r = Variable(self.value.expand(sizes)) # take the value and return a tensor that in the shape of sizes
        print(f'{r.name} = {self.name}.expand({sizes})')
        def propagate(dL_doutputs):
            dL_dr, = dL_doutputs
            return [dL_dr.sum()]
        gradient_tape.append(TapeEntry(inputs=[self.name], outputs=[r.name], propagate=propagate))
        return r

class TapeEntry(NamedTuple):
    """
    input and outputs are unique names of the Variables that are 
    inputs and outputs of the original computation
    """
    inputs: List[str]
    outputs: List[str]
    
    """
    propagate is a closure that propagates the gradient of the outputs of this function
    to the inputs using the chain rule - which is specific to each leaf operaton which is spceific
    
    this is specific to each leaf operator - its inputs dL/dOutputs, dL/dInputs  
    """
    propagate: 'Callable[List[Variable], List[Variable]]'
    
    
# the tape is just a list of accumulated entries recording all compute   
gradient_tape: List[TapeEntry] = []
def reset_tape():
    gradient_tape.clear()
    global _name
    _name = 0 # reset variable names too to keep them small.
    
"""
Now that everythings has been sufficiently defined
- lets see how we put the pieces together
"""

def grad(L, desired_results: List[Variable]) -> List[Variable]:
    # this map holds dL/dX for all values X 
    # recall that the first gradient with respect to loss is just 1 -> dL/dL 
    dL_d: Dict[str, Variable] = {L.name: Variable(torch.ones(()))}
    print(f'd{L.name} ------------------------')
    def gather_grad(entries:List[str]):
        """ 
        Fetches the gradients for the given entries or None if they are not used to compute the loss
        
        We define an unused element gradient as None because it allows us to quickly check that the gradient value is Zero
        so later on when we are propagating we can skip the propagate function call
        
        How does this Skipping optimization work?
        Look at the comment in line 220
        """
        return [dL_d[entry] if entry in dL_d else None for entry in entries]
    
    for entry in reversed(gradient_tape):
        dL_doutputs = gather_grad(entry.outputs)
        if all(dL_doutput is None for dL_doutput in dL_doutputs):
            # So why do we have this check here? 
            # recall the following:
            # Let us have a vector valued function y = f(x) where y and x are vectors
            # The gradient of y with respect x where x is n dimensional corresponds to the Jacobian matrix J:
            # J = ( dy/x_1, dy/x_2, .. dy/x_n) = (dy_1/dx_1 .. dy1/dx_n)
            #                                    (dy_2/dx_2 ... dy2/dx_n)
            #                                    (...............dy_m/dx_n)
            # Generally speaking this is what torch.autograd does -> its an engine for computing vector-Jacobian products 
            # Or in other words given a vector v, we compute the product J^T * v
            # If v is the gradient with respect to L
            # Then by definition the product of v* the jacobian gives us the gradient of L with respect to x
            # J^T * x= (dy_1/dx_1 * dl/d_y1 == dl/dx_1 and so forth for all matrix mults)
            
            # So this is great and all but during our task we try not construct the jacobian matrix because it often has a lot of computational
            # costs associated with it ->  so to cut corners if by the rules of matrix multiplication if x = 0 then since matrix mult is linear
            # then J^t * x = should also be 0 and thats why we have that check for None there 
            # theoretically we could have a grad tensor of 0's but then we'd have to iterate over them to check
            continue
        
        # effectively we compute the change in gradients for the input of the current node this way
        dL_dinputs = entry.propagate(dL_doutputs)
        for input, dL_dinput in zip(entry.inputs, dL_dinputs):
            # and here we instead of adding it to p.grad -> we accumulate the gradients in our change map above
            if input not in dL_d:
                dL_d[input] = dL_dinput
            else:
                dL_d[input] += dL_dinput
            
        # print some information to understand the values of each intermediate 
        for name, value in dL_d.items():
            print(f'd{L.name}_d{name} = {value.name}')
        print(f'------------------------')
        
        ## Note that it follows the same structure as Karpathy's training loop - just instead
        ## we set a bit of groundwork seeidng the map and recursively calculate gradients via 
        ## our reversed tape rather than calling build_topo(v) like how we do in our backward function
    return gather_grad(desired.name for desired in desired_results)
 