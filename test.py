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
