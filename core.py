class ExecutionBlock:
    def __init__(self, stack, queue):
        self.stack = stack
        self.queue = queue
        self.maxIndex = len(queue)-1
        self.pointerIndex = 0

    def execute(self):
        while self.pointerIndex <= self.maxIndex:
            func = self.queue[self.pointerIndex]
            self.pointerIndex += 1
            newP = func(self.stack, self.queue, self.pointerIndex)
            if newP != None : self.pointerIndex = newP

# System Functions
def push(stack, queue, index):
    stack.append(queue[index])
    return index+1

def run(stack, queue, index):
    e = ExecutionBlock(stack, runtimeFn[queue[index]])
    e.execute()
    return index+1

def jumpIndex(stack, queue, index):
    return queue[index]

def jumpZero(stack, queue, index):
    return (index+1,queue[index])[stack.pop()==0]

# Runtime Functions
def add(stack, queue, index):
    v2 = stack.pop()
    v1 = stack.pop()
    res = v1 + v2
    stack.append(res)

def minus(stack, queue, index):
    v2 = stack.pop()
    v1 = stack.pop()
    res = v1 - v2
    stack.append(res)

def multiply(stack, queue, index):
    v2 = stack.pop()
    v1 = stack.pop()
    res = v1 * v2
    stack.append(res)

def divide(stack, queue, index):
    v2 = stack.pop()
    v1 = stack.pop()
    res = v1 // v2
    stack.append(res)

def equalCond(stack, queue, index):
    v2 = stack.pop()
    v1 = stack.pop()
    if v1 == v2:
        stack.append(1)
    else:
        stack.append(0)

def equalZeroCond(stack, queue, index):
    v1 = stack.pop()
    if v1 == 0:
        stack.append(1)
    else:
        stack.append(0)

def swap(stack, queue, index):
    v2 = stack.pop()
    v1 = stack.pop()
    stack.append(v2)
    stack.append(v1)

def duplicate(stack, queue, index):
    stack.append(stack[len(stack)-1])

def show(stack, queue, index):
    print(stack)

def pop(stack, queue, index):
    res = stack.pop()
    print(res)

def drop(stack, queue, index):
    stack.pop()


# Compile functions
def cDefine(comp, cStack, queue):
    if cStack:
        raise ": error"
    label = comp.getToken()
    cStack.append((":", label))

def cEnd(comp, cStack, queue):
    if not cStack:
        raise "No : for ;"
    code, label = cStack.pop()
    if code != ":":
        raise "No : for ;"
    runtimeFn[label] = queue[:]
    while queue:
        queue.pop()

def cIf(comp, cStack, queue):
    queue.append(jumpZero)
    cStack.append(("if", len(queue)))
    queue.append(0)

def cElse(comp, cStack, queue):
    if not cStack:
        raise "No if for else"
    code, slot = cStack.pop()
    if code != "if":
        raise "else not preceded by if"
    queue.append(jumpIndex)
    cStack.append(("else",len(queue)))
    queue.append(0)
    queue[slot] = len(queue)

def cThen(comp, cStack, queue):
    if not cStack:
        raise "No if or else for then"
    code, slot = cStack.pop()
    if code not in ("if", "else"):
        raise "then not preceded by if or else"
    queue[slot] = len(queue)

def cBegin(comp, cStack, queue):
    cStack.append(("begin", len(queue)))

def cUntil(comp, cStack, queue):
    if not cStack:
        raise
    code, slot = cStack.pop()
    if code != "begin":
        raise
    queue.append(jumpZero)
    queue.append(slot)


# def cDo(comp, cStack, queue):
#     idx = queue.pop()
#     ctrl = queue.pop()
#     comp.loopStack.append(ctrl)
#     comp.loopStack.append(idx)
#     cStack.append(("do", len(queue)))

# def cLoop(comp, cStack, queue):
#     if not cStack:
#         raise
#     code, slot = cStack.pop()
#     if code != "do":
#         raise
    
#     idx = queue.pop()
#     ctrl = queue.pop()
#     comp.loopStack.append(ctrl)
#     comp.loopStack.append(idx+1)

#     queue.append(jumpZero)
#     queue.append(slot)

# Maps
systemFn = {
    "push": push,
    "run": run,
    "jumpZero": jumpZero,
    "jumpIndex": jumpIndex,
}

runtimeFn = {
    "+": add,
    "-": minus,
    "*": multiply,
    "/": divide,

    "=": equalCond,
    "0=": equalZeroCond,

    "swap": swap,
    "dup": duplicate,
    "drop": drop,

    ".": pop,
    ".s": show,

}

compileFn = {
    ":": cDefine,
    ";": cEnd,
    "if": cIf,
    "else": cElse,
    "then": cThen,
    "begin": cBegin,
    "until": cUntil,

}


