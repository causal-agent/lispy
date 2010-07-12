TODO List
=========

Features
--------

 * Python interop
 * <del>Destructive set functions (`set!`, etc)</del>
 * Destructuring

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
 * <del>Allow optional arguments to have default values</del>
 * Make all arguments after `?` optional

Python Core
-----------

 * <del>Type predicates (`list?`, `macro?`, etc)</del>

Lisp Core
---------

 * <del>Fix `reduce` somehow (does not work for `t`/`nil` stuff)</del>
 * <del>Fix `reverse` (possibly a problem in `append`)</del>

Scope
-----

