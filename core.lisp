;; Lisp Core definitions for Lispy

;; Define Macros
(def defmacro (macro (n a b) `(def ,n (macro ,a ,b))))
(defmacro defun (n a b) `(def ,n (fn ,a ,b)))
(def defn defun)

;; Logical operators
(defmacro and (x y) `(cond (,x (cond (,y t) (t nil))) (t nil)))
(defmacro not (x) `(cond (,x nil) (t t)))
(defmacro nand (x y) `(not (and ,x ,y)))
(defmacro or (x y) `(nand (nand ,x ,x) (nand ,y ,y)))
(defmacro xor (x y) `(or (and ,x (not ,y)) (and (not ,x) ,y)))

;; Common Functions
(defmacro caar (x) `(car (car ,x)))
(defmacro cadr (x) `(car (cdr ,x)))
(defmacro caddr (x) `(car (cdr (cdr ,x))))
(defmacro cadar (x) `(car (cdr (car ,x))))
(defmacro caddar (x) `(car (cdr (cdr (car ,x)))))

;; Predicates
(defun nil? (x)
  (or (= x '()) (= x nil)))

;; More normal flow control
(defmacro if (p x y) `(cond (,p ,x) (t ,y)))
;(defmacro when (p & b) `(if ,p (do ,@b) nil))

;; Append
(defun append (x y)
  (if (nil? x)
    y
    (cons (car x) (append (cdr x) y))))

;; Reduce, one of the great FP functions
(defun reduce (f l)
  (if (nil? l)
    (f)
    (f (car l) (reduce f (cdr l)))))

;; Filter
(defun filter (f l)
  (if (nil? l)
    l
    (if (f (car l))
      (append (car l) (filter f (cdr l)))
      (filter f (cdr l)))))

;; Apply
;(defmacro apply (f l) `(,f ,@l))
