# simple-pl
A simple interpreted programming language (to Python)

Usage examples:

Define an expression as (operand variable1 variable2 (if present))
E.g.:
  (var a 1)
    (var b (+ a 1))
    (do 
        (var a (+ b 5))
        (set b (+ a 10))
    )
    (* a b)

Parser will convert to recursive tree of expressions, represented as array.
For each expression, corresponding Python logic will be called.
