from state import State

class ErrState(State):
  	
    isEnd = True

    def render(self):
        output = "You reached the end with an Error!"
        return output
    
    def process(self, input):
        if self._validateInput(input):
            funcName = self.acceptInput[input]['action']
            func = getattr(self, funcName, None)
            return func()
        else:
            print "Not valid Input! \n"
            return self.name, self.data
