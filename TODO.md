TODO List
=========

Features
--------

 * Python interop
 * <del>Destructive set functions (`set!`, etc)</del>

Documentation
-------------

 * <del>Document Python Core functions</del>
 * Document Lisp Core functions
 * Document syntax
   * Lambda argument syntax (`?` `&`)

Reader
------

 * Make quotes able to read more than just symbols and lists (allow
   quoting of anything using the quote reader macros)

AST
---

### Lambda

 * Do something to improve recursion
 * <del>Prevent new scopes being created on recursion</del>
 * <del>Allow `&` arguments to accept nothing</del>
 * Allow optional arguments to have default values

Python Core
-----------

Lisp Core
---------

 * Fix `reduce` somehow (does not work for `t`/`nil` stuff)
 * Fix `reverse` (possibly a problem in `append`)

Scope
-----

