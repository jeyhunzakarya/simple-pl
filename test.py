from evaluator import pl_eval
from parser import pl_parse_prog

def tester():
    expr = '''
    (var a 1)
    (var b (+ a 1))
    (do 
        (var a (+ b 5))
        (set b (+ a 10))
    )
    (* a b)
'''
    print(pl_eval(None, pl_parse_prog(expr)))

    function_test = '''
    (def fib (n) (
        do 
        (var r 0)
        (loop (gt n 0) (do
            (set r (+ r n))
            (set n (- n 1))
        ))
        (return r)
    ))
    (call fib 5)
'''
    print(pl_eval(None, pl_parse_prog(function_test)))
