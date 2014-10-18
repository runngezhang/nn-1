import os
USE_GPU = True
if 'GNUMPY_USE_GPU' in os.environ:
    if os.environ['GNUMPY_USE_GPU'] == 'no':
        USE_GPU = False
if not USE_GPU:
    import numpy as gnp
    gnp.random.seed(19)
else:
    import gnumpy as gnp

'''
Ideally hide away all low-level libraries so easier to swap one library
out with another for later optimization

Currently using gnumpy on top of cudamat, with option to use CPU instead
'''

# Convert numpy / other array to type we'll use

def array(arr):
    # Just used to put back on GPU
    if USE_GPU:
        return gnp.garray(arr)
    else:
        return arr

def as_np(arr):
    if USE_GPU:
        return arr.as_numpy_array()
    else:
        return arr

def empty(shape):
    return gnp.empty(shape)

def rand(shape, rg=[0, 1]):
    if USE_GPU:
        return gnp.rand(shape) * (rg[1] - rg[0]) + rg[0]
    else:
        return gnp.random.rand(*shape) * (rg[1] - rg[0]) + rg[0]

def zeros(shape):
    return gnp.zeros(shape)

def ones(shape):
    return gnp.ones(shape)

# Nonlinearities

def relu(x):
    return x * (x > 0)

def sigmoid(x):
    if USE_GPU:
        return x.logistic()
    else:
        return 1 / (1 + gnp.exp(-x))

def tanh(x):
    if USE_GPU:
        return x.tanh()
    else:
        return gnp.tanh(x)

def exp(x):
    if USE_GPU:
        return x.exp()
    else:
        return gnp.exp(x)

def get_nl(nl):
    if nl == 'relu':
        return relu
    elif nl == 'sigmoid':
        return sigmoid
    elif nl == 'tanh':
        return tanh
    else:
        assert False, 'No such nonlinearity: %s' % nl

def get_nl_grad(nl, act):
    if nl == 'relu':
        return act > 0
    elif nl == 'sigmoid':
        return act * (1 - act)
    elif nl == 'tanh':
        return (1 - act*act)
    else:
        assert False, 'No such nonlinearity: %s' % nl


# Matrix multiply

def mult(A, B):
    return gnp.dot(A, B)
