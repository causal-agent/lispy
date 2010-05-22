# Copyright 2010 Curtis (Programble) <programble@gmail.com>
# Licensed under the GNU GPLv3

from scope import Scope
import lisp

global_scope = Scope()

# Core bindings
global_scope["t"] = lisp.Symbol("t")
t = global_scope["t"]
global_scope["nil"] = lisp.Symbol("nil")
nil = global_scope["nil"]

# Core functions

def atom(scope, x):
    """atom(x) is True if x is an Atom"""
    if x.__class__ != lisp.Atom:
        x = x.evaluate(scope)
    return x.__class__ == lisp.Atom
global_scope["atom"] = atom

def eq(scope, x, y):
    """eq(x, y) is True is x and y are equal"""
    if x.__class__ != lisp.Atom:
        x = x.evaluate(scope)
    if y.__class__ != lisp.Atom:
        y = y.evaluate(scope)
    if x == y:
        return t
    else:
        return nil
global_scope["eq"] = eq

def car(scope, x):
    """car(x) is the first item of x if x is non-atomic"""
    return x.evaluate(scope).car()
global_scope["car"] = car

def cdr(scope, x):
    """cdr(x) is the rest of x if x is non-atomic"""
    return x.evaluate(scope).cdr()
global_scope["cdr"] = cdr

def cons(scope, x, y):
    """cons"""
    if x.__class__ != lisp.Atom:
        x = x.evaluate(scope)
    if y.__class__ != lisp.Atom:
        y = y.evaluate(scope)
    return y.cons(x)
global_scope["cons"] = cons

def cond(scope, *x):
    """cond"""
    for test in x:
        if test.car().evaluate(scope) == t:
            ret = test.cdr().car()
            if ret.__class__ != lisp.Atom:
                ret = ret.evaluate(scope)
            return ret
    return nil
global_scope["cond"] = cond

def quote(scope, x):
    """quote"""
    return x
global_scope["quote"] = quote

def def_(scope, symbol, x):
    # Can only bind to a symbol
    if symbol.__class__ != lisp.Symbol:
        return nil
    if x.__class__ != lisp.Atom:
        x = x.evaluate(scope)
    scope[symbol.data] = x
    return scope[symbol.data]
global_scope["def"] = def_

def lambda_(scope, names, *body):
    l = lisp.Lambda(names, body)
    return l
global_scope["lambda"] = lambda_

def backquote(scope, expr):
    if expr.__class__ != lisp.List:
        return expr
    new = []
    for x in expr.data:
        if x.__class__ == lisp.List:
            # Evaluate only unquoted items
            if x.car() == lisp.Symbol("unquote"):
                new.append(x.cdr().car().evaluate(scope))
            else:
                new.append(backquote(scope, x))
        else:
            new.append(x)
    return lisp.List(new)
global_scope["backquote"] = backquote

def macro(scope, names, *body):
    m = lisp.Macro(names, body)
    return m
global_scope["macro"] = macro

def macroexpand(scope, expr):
    if expr.__class__ != lisp.List:
        return expr
    if expr.car().__class__ != lisp.Symbol:
        return expr
    m = expr.car().evaluate(scope)
    if m.__class__ != lisp.Macro:
        return expr
    return lisp.Lambda.fn(m, scope, *expr.cdr().data)
global_scope["macroexpand"] = macroexpand

def let(scope, bindings, *exprs):
    # Create a new scope
    local_scope = Scope(scope)
    # Bind each pair in bindings
    for pair in bindings.data:
        x = pair.cdr().car()
        if x.__class__ != lisp.Atom:
            x = x.evaluate(local_scope)
        local_scope[pair.car().data] = x
    # Evaluate each expr in local scope
    for expr in exprs[:-1]:
        expr.evaluate(local_scope)
    # Return the result of the last expr
    return exprs[-1].evaluate(local_scope)
global_scope["let"] = let

# Arithmetic functions

def add(scope, *x):
    ret = 0
    for i in x:
        if i.__class__ != lisp.Atom:
            i = i.evaluate(scope)
        ret += i.evaluate(scope)
    return lisp.Atom(ret)
global_scope["+"] = add

def sub(scope, *x):
    ret = 0
    for i in x:
        if i.__class__ != lisp.Atom:
            i = i.evaluate(scope)
        ret -= i.evaluate(scope)
    return lisp.Atom(ret)
global_scope["-"] = sub

def mul(scope, *x):
    ret = 1
    for i in x:
        if i.__class__ != lisp.Atom:
            i = i.evaluate(scope)
        ret *= i.evaluate(scope)
    return lisp.Atom(ret)
global_scope["*"] = mul

def div(scope, *x):
    if len(x) == 1:
        x = x[0]
        if x.__class__ != lisp.Atom:
            x = x.evaluate(scope)
        return 1 / x.evaluate(scope)
    if x[0].__class__ != lisp.Atom:
        x[0] = x[0].evaluate(scope)
    ret = x[0]
    for i in x[1:]:
        if i.__class__ != lisp.Atom:
            i = i.evaluate(scope)
        ret /= i.evaluate(scope)
    return lisp.Atom(ret)
global_scope["/"] = div
