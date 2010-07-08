Core Functions
==============

Python Core
-----------

Documentation on core functions implemented in Python

### quote

    (quote x)

Prevents its argument from being evaluated. The reader macro `'`
expands to this function.

    => (quote x)
    x
    => 'x
    x

### eval

    (eval x)

Evaluates its argument (twice). Can be used to evaluate quoted data.

    => (eval (quote eval))
    <function eval at 0x87a34c4>

### ==

    (== x y)

Tests its two arguments for equality. Evaluates to `t` on equality and
`nil` otherwise.

    => (== 1 2)
    nil
    => (== 1 1)
    t

### car

    (car xs)

Evaluates to the `car` of the list `xs`. The `car` is the first item
of the list. If the list is empty, evaluates to `nil`.

    => (car '(1 2 3))
    1
    => (car '())
    nil

### cdr

    (cdr xs)

Evaluates to the `cdr` (rest) of the list `xs`. If the list is empty
or contains only one item, evaluates to `nil`. For proper lists,
always evaluates to another list. For improper lists, evaluates to one
value.

    => (cdr '(1 2 3))
    (2 3)
    => (cdr '(1))
    nil
    => (cdr '())
    nil
    => (cdr '(1 . 2))
    2

### cons

    (cons x y)

Evaluates to a new cons list in which `x` is the car and `y` is the
cdr.

    => (cons 1 2)
    (1 . 2)
    => (cons 1 (cons 2 nil))
    (1 2)

### cond

    (cond & clauses)

For each clause supplied, the car of the clause is evaluated, and if
non-nil, the cdr is returned, or if the clause has only one item, the
car is returned. Clauses are evaluated in order, and evaluation stops
after the first clause evaluates non-nil. If no clauses evaluate to
non-nil, `nil` is returned.

    => (cond (nil 1) (nil 2) (t 3))
    3
    => (cond (nil 1) (nil 2) (nil 3))
    nil

### def

    (def name value)

Binds `name` to `value` in the global scope. Evaluates to `name` if
the binding succeeds, otherwise evaluates to `nil`. Binding will fail
if `name` is not a symbol, or `name` has already been bound in the
global scope.

    => (def x 1)
    x
    => x
    1
    => (def x 2)
    nil

### undef!

    (undef! name)

Unbinds `name` in the global scope. Evaluates to the value of `name`,
or `nil` if `name` was not bound.

    => (def x 1)
    x
    => (undef! x)
    1
    => (undef! y)
    nil

### set!

    (set! name value)

Rebinds `name` in the scope it is bound in to `value`. Evaluates to
the previous value of `name`, or `nil` if `name` is not bound.

    => (def x 1)
    x
    => (set! x 2)
    1
    => x
    2
    => (set! y 3)
    nil

### unset!

    (unset! name)

Unbinds `name` in the scope it is bound in. Evaluates to the value of
`name` or `nil` if `name` is not bound.

    => (def x 1)
    x
    => (unset! x)
    1
    => (unset! y)
    nil

