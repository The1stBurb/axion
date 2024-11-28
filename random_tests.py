

lvl_txt = "`1[I love the sea!]`34[Explosions are tasty]`5[literally nobody cares]"



messages = {}
idx = ""
msg = ""
mode=0
for char in lvl_txt:
    if char == "`":
        mode = 1
    elif mode == 1:
        if char == "[":
            mode = 2
            continue
        idx += char
    elif mode == 2:
        if char == "]":
            mode = 0
            messages[int(idx)] = msg
            idx = ""
            msg = ""
            continue
        msg += char


print(messages)
write = ""

for key in messages:
    write += f"`{key}[{messages[key]}]"

print(write)

messages = {}
idx = ""
msg = ""
mode=0
for char in write:
    if char == "`":
        mode = 1
    elif mode == 1:
        if char == "[":
            mode = 2
            continue
        idx += char
    elif mode == 2:
        if char == "]":
            mode = 0
            messages[int(idx)] = msg
            idx = ""
            msg = ""
            continue
        msg += char

print(messages)