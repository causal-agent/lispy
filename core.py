# Copyright 2010 Curtis McEnroe <programble@gmail.com>
# Licensed under the GNU GPLv3

from scope import Scope
from ast import *

# The global scope
scope = Scope()

# Core bindings

# t is t is t is t
t = Symbol("t")
scope["t"] = t

# nil is nil (but also the empty list)
nil = Symbol("nil")
scope["nil"] = nil

# Lispy information
scope["*lispy-version*"] = List([Number(0), Number(2), Number(0), []])

# Core core functions

def quote(scope, x):
    return x
scope["quote"] = quote

def eq(scope, x, y):
    x, y = x.evaluate(scope), y.evaluate(scope)
    if x == y:
        return t
    else:
        return nil
scope["eq"] = eq
scope["="] = eq

def car(scope, x):
    return x.evaluate(scope).car()
scope["car"] = car

def cdr(scope, x):
    return x.evaluate(scope).cdr()
scope["cdr"] = cdr

def cons(scope, x, y):
    x, y = x.evaluate(scope), y.evaluate(scope)
    if y == nil:
        return List([x, []])
    elif y.__class__ == List:
        return List([x] + y.data)
    else:
        return List([x, y])
scope["cons"] = cons

def cond(scope, *x):
    for clause in x:
        if clause.cdr() == List([]) and clause.car().evaluate(scope) != nil:
            return clause.car().evaluate(scope)
        if clause.car().evaluate(scope) != nil:
            for expr in clause.cdr().data[:-2]:
                expr.evaluate(scope)
            return clause.cdr().data[-2].evaluate(scope)
    return nil
scope["cond"] = cond

# Core special forms

def def_(local, symbol, value):
    # Can only bind to a symbol
    if symbol.__class__ != Symbol:
        return nil
    # Evaluate value
    value = value.evaluate(scope)
    # Bind in global scope
    scope[symbol.data] = value
    return local[symbol.data]
scope["def"] = def_

def lambda_(scope, names, *body):
    return Lambda(names, body)
scope["lambda"] = lambda_

# Macro functions

def syntax_quote(scope, expr):
    if expr.__class__ != List:
        return expr
    new = []
    for x in expr.data:
        if x.__class__ == List:
            # Evaluate only unquoted items
            if x.car() == Symbol("unquote"):
                new.append(x.cdr().car().evaluate(scope))
            elif x.car() == Symbol("unquote-splice"):
                l = x.cdr().car().evaluate(scope)
                for i in l.data[:-1]:
                    new.append(i)
            else:
                new.append(syntax_quote(scope, x))
        else:
            new.append(x)
    return List(new)
scope["syntax-quote"] = syntax_quote

def macro(scope, names, *body):
    return Macro(names, body)
scope["macro"] = macro

# Other core functions

def list_(scope, *x):
    return List([i.evaluate(scope) for i in x] + [[]])
scope["list"] = list_

def let(scope, bindings, *exprs):
    local = Scope(scope)
    for pair in bindings.data[:-1]:
        local[pair.car().data] = pair.cdr().car().evaluate(local)
    for expr in exprs[:-1]:
        expr.evaluate(local)
    return exprs[-1].evaluate(local)
scope["let"] = let

def do(scope, *exprs):
    for expr in exprs[:-1]:
        expr.evaluate(scope)
    return exprs[-1].evaluate(scope)
scope["do"] = do

def dolist(scope, nl, *exprs):
    ret = nil
    # Create new local scope
    local_scope = Scope(scope)
    # Evaluate the list
    l = nl.cdr().car().evaluate(scope)
    for i in l.data[:-1]:
        # Bind this item to the name
        local_scope[nl.car().data] = i.evaluate(scope)
        for expr in exprs:
            ret = expr.evaluate(local_scope)
    return ret
scope["dolist"] = dolist

# Arithmetic functions

def add(scope, *x):
    if len(x) == 0:
        return 0
    if len(x) == 1:
        return x[0]
    else:
        return add(scope, Number(x[0].evaluate(scope).data + x[1].evaluate(scope).data), *x[2:])
scope["+"] = add

def sub(scope, *x):
    if len(x) == 0:
        return 0
    if len(x) == 1:
        return x[0]
    else:
        return sub(scope, Number(x[0].evaluate(scope).data - x[1].evaluate(scope).data), *x[2:])
scope["-"] = sub

def mul(scope, *x):
    if len(x) == 0:
        return 1
    if len(x) == 1:
        return x[0]
    else:
        return mul(scope, Number(x[0].evaluate(scope).data * x[1].evaluate(scope).data), *x[2:])
scope["*"] = mul

def div(scope, *x):
    if len(x) == 0:
        return 0
    if len(x) == 1:
        return x[0]
    else:
        return div(scope, Number(x[0].evaluate(scope).data / x[1].evaluate(scope).data), *x[2:])
scope["/"] = div

def mod(scope, x, y):
    x = x.evaluate(scope)
    y = y.evaluate(scope)
    return Number(x.data % y.data)
scope["%"] = mod

# Comparison Operators

def lt(scope, x, y):
    x = x.evaluate(scope)
    y = y.evaluate(scope)
    if x.data < y.data:
        return t
    else:
        return nil
scope["<"] = lt

def gt(scope, x, y):
    x = x.evaluate(scope)
    y = y.evaluate(scope)
    if x.data > y.data:
        return t
    else:
        return nil
scope[">"] = gt
