
def pl_eval(env, node):
    if len(node) == 0:
        raise ValueError("empty node")

    ###Variable lookup###
    if not isinstance(node, list):
        assert isinstance(node, str) #a variable name; so have to look up from closure env
        return name_lookup(env, node)[node]

    ###Value###
    if len(node) == 2 and node[0] == "val": #case val
        return node[1]
    import operator

    ###Binary operations###
    binops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        "eq": operator.eq,
        "ne": operator.ne,
        "ge": operator.ge,
        "le": operator.le,
        "gt": operator.gt,
        "lt": operator.lt,
        "and": operator.and_,
        "or": operator.or_
    }

    if len(node) == 3 and node[0] in binops:
        operand = binops[node[0]]
        return operand(pl_eval(env, node[1]), pl_eval(env, node[2]))
    
    ###Unary operations###
    unops = {
        "-": operator.neg,
        "!": operator.not_
    }

    if len(node) == 2 and node[0] in unops:
        operand = unops[node[0]]
        return operand(pl_eval(node[1]))

    ###Conditional###
    if len(node) in [3,4] and node[0] in ["?", "if"]:
        _, cond, yes, *no = node
        no = no[0] if no else ["val", None] #handle the else part being optional
        new_env = (dict(), env) # Define a new inner env for the conditional's scope. This way if a var is defined in cond, it will be added to new_env, and can be accessed from inside the scope

        if (pl_eval(cond)):
            return pl_eval(new_env, yes)
        else:
            return pl_eval(new_env, no)
    if (node[0]) == "print":
        return print(*(pl_eval(val) for val in node[1:]))

    ###Sequential expressions###
    if node[0] in ["do", "then", "else"]: # a new scope, with a sequence of expressions. a new env is created for this scope.It will have parent's env, but also inner values, that are not in parent's env
        new_env = (dict(), env)  # notice the simplicity of the env data structure, and manipulation logic. Just define a tuple, and all the parent level logic is managed by recursion
        for val in node[1:]: #first entry in the expression is just do or its alias, so no need to pass it
            val = pl_eval(new_env, val)  
        return val # since it is a sequence of operations, and we only need the last expression's result, just return that. Notice the elegance of env again: no need to update new_env or anything here, or explicitly handle state communication between consecutive expressions. All of that is handled by new_env

    ###Variables###
    if node[0] == "var" and len(node) == 3: # first is var keyword, second is var name third is value. Notice val can be ref to var by itself too.
        _, name, value = node
        scope, _ = env
        if name in scope:
            raise ValueError("var already exists")
        value = pl_eval(env, value)
        scope[name] = value # add key value pair to the env
        return value
    
    if node[0] == "set" and len(node) == 3:
        _, name, value = node
        scope = name_lookup(env, name)
        value = pl_eval(env, value)
        scope[name] = value
        return value               

    ###Loop###
    if node[0] == "loop" and len(node) == 3:
        _, cond, body = node

        ret = None
        while True:
            new_env = (dict(), env)
            if not pl_eval(new_env, cond):
                break
            try:
                ret = pl_eval(new_env, body)
            except LoopBreak:
                break
            except LoopContinue:
                continue
        return ret

    if node[0] == "break" and len(node) == 1:
        raise LoopBreak
    if node[0] == "continue" and len(node) == 1:
        raise LoopContinue

    ###Function###
    if node[0] == "def" and len(node) == 4:
        _, name, args, body = node
            
        for argname in args:
            if not isinstance(argname, str):
                raise ValueError("bad argument name")
        if len(args) != len(set(args)):
            raise ValueError("duplicate arg names")

        key = (name, len(args)) #Same function but different args count - still valid
        dct, _ = env #Notice that, we are only checking the func name in the current env. This is because even if parent has the same name function, the inner function will simply override it in inner scope.
        if key in dct:
            raise ValueError("function already exists")
        dct[key] = (args, body, env) #Notice the usefulness of tuple here, as it allows multiple items of different types to be stored together, as well as easy destructuring. Also notice that, we are storing the env here as well. This is because, a function is essentially a closure - even if used somewhere else, it will still have reference to the scope where it is defined.
        return
    
    if node[0] == "call" and len(node) >= 2: #At least call and function name, args optional
        new_env = dict()
        _, name, *args = node
        key = (name, len(args))
        fargs, fbody, fenv = name_lookup(env, key)[key] #notice we don't use env here, but fenv from lookup table: that is because as mentioned before, functions are closures
        for arg_name, arg_val in  zip(fargs, args):
            new_env[arg_name] = pl_eval(env, arg_val) #it is possible that the arg is an expression itself
        try:
            ret = pl_eval((new_env, fenv), fbody)
            return ret
        except FuncReturn as ret:
            return ret.val

    if node[0] == "return" and len(node) == 1:
        raise FuncReturn(None)
    if node[0] == "return" and len(node) == 2:
        raise FuncReturn(pl_eval(env, node[1]))

    ###Else - Invalid###
    raise ValueError("invalid expression")

class LoopBreak(Exception):
    def __init__(self):
        super().__init__('break outside a loop')

class LoopContinue(Exception):
    def __init__(self):
        super().__init__('continue outside a loop')

class FuncReturn(Exception):
    def __init__(self, val):
        super().__init__('Return outside function')
        self.val = val

def name_lookup(env, key):
    while env:
        current, env = env
        if key in current:
            return current #returns the env
    raise ValueError("var not defined")
