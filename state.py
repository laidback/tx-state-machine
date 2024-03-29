class State(object):
    
    data = None
    isStart = False
    isEnd = False
    name = '' 
    acceptInput = {}
    actInput = ''
    
    def __init__(self, name, transition={}): 
        """Initialize state.""" 
        self.name = name 
        self.acceptInput = transition
    
    def __call__(self, input):
        return self
    
    def render(self): 
        raise NotImplementedError()
    
    def process(self, input):
        raise NotImplementedError()
    
    def _validateInput(self, input):
        if input in self.acceptInput:
            return True
        return False
