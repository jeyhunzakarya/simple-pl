
def pl_eval(env, node):
    if not isinstance(node, list):
        assert isinstance(node, str) #a variable name; so have to look up from closure env
        return name_lookup(env, node)[node]

    if len(node) == 0:
        raise ValueError("empty node")
    if len(node) == 2 and node[0] == "val": #case val
        return node[1]
    import operator

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
    
    unops = {
        "-": operator.neg,
        "!": operator.not_
    }

    if len(node) == 2 and node[0] in unops:
        operand = unops[node[0]]
        return operand(pl_eval(node[1]))

    if len(node) == 4 and node[0] == "?":
        _, cond, yes, no = node

        if (pl_eval(cond)):
            return pl_eval(yes)
        else:
            return pl_eval(no)
    if (node[0]) == "print":
        return print(*(pl_eval(val) for val in node[1:]))

    if node[0] in ["do", "then", "else"]: # a new scope, with a sequence of expressions. a new env is created for this scope.It will have parent's env, but also inner values, that are not in parent's env
        new_env = (dict(), env)  # notice the simplicity of the env data structure, and manipulation logic. Just define a tuple, and all the parent level logic is managed by recursion
        for val in node[1:]: #first entry in the expression is just do or its alias, so no need to pass it
            val = pl_eval(new_env, val)  
        return val # since it is a sequence of operations, and we only need the last expression's result, just return that. Notice the elegance of env again: no need to update new_env or anything here, or explicitly handle state communication between consecutive expressions. All of that is handled by new_env

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

    raise ValueError("invalid expression")

def name_lookup(env, key):
    while env:
        current, env = env
        if key in current:
            return current #returns the env
    raise ValueError("var not defined")
