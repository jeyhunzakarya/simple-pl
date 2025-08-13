from utils import skip_space_extended

def pl_parse_prog(s):
    return pl_parse("(do" + s +")")

def pl_parse(s):
    idx, node = parse_expr(s, 0)
    idx = skip_space_extended(s, idx)
    if idx < len(s):
        raise ValueError('trailing emptyspace')
    return node

def parse_atom(s):
    import json
    try:
        return ['val', json.loads(s)]
    except json.JSONDecodeError:
        return s 

def parse_expr(s:str, idx: int):
    idx = skip_space_extended(s, idx)
    if s[idx] == "(":
        #valid start
        idx += 1
        l = []
        while True:
            idx = skip_space_extended(s, idx)
            if idx >= len(s):
                raise Exception("length limit")
            else:
                if s[idx] == ")":
                    idx += 1
                    break

            idx, v = parse_expr(s, idx)
            l.append(v)
        return idx, l  

    elif s[idx] == ")":
        raise Exception("bad parenthesis")
        #invalid
    else:
        start = idx
        while idx < len(s) and (not s[idx].isspace()) and s[idx] not in "()":
            idx += 1
        if start == idx:
            raise Exception("empty program")
        return idx, parse_atom(s[start:idx])
