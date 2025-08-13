def skip_space(s: str, idx: int):
    while idx < len(s) and s[idx].isspace():
        idx += 1
    return idx

def skip_space_extended(s: str, idx: int):
    while True:
        save = idx

        while idx < len(s) and s[idx].isspace(): #only whitespace
            idx += 1

        if idx < len(s) and s[idx] == ";": #encountered the end of code; remove the comments coming after it
            while idx < len(s) and s[idx] != "\n":
                idx += 1
        if idx == save: #nothing changed in last loop iteration, so nothing to remove
            break
    return idx
