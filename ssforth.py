import core as c

class Forth:
    def __init__(self):
        self.stack = []
        self.cStack = []
        self.input = []

    def getToken(self, prompt="... "):
        while not self.input: 
            try: 
                lin = input(prompt)+"\n"
            except: 
                return None
            self.input.extend(lin.lower().split())
            
        token = self.input[0]
        del self.input[0]
        return token

    def run(self):
        while True:
            code = self.compile()
            e = c.ExecutionBlock(self.stack, code)
            e.execute()

    def compile(self):
        prompt = "SuperSeriousForth > "
        code = []
        while True:
            token = self.getToken(prompt)

            cFunction = c.compileFn.get(token)
            rFunction = c.runtimeFn.get(token)

            if cFunction:
                cFunction(self, self.cStack, code)
            elif rFunction:
                if type(rFunction) == type([]):
                    code.append(c.systemFn.get("run"))
                    code.append(token)
                else:
                    code.append(rFunction)
            else:
                code.append(c.systemFn.get("push"))
                try:
                    code.append(int(token))
                except:
                    code[-1] = c.systemFn.get("run")

            if not self.cStack:
                return code

            prompt = "...   "







if __name__ == "__main__":
    main = Forth()
    main.run()