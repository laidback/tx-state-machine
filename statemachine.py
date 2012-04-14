#!/usr/env python2.7
# -*- coding: utf-8 *-*

""" StateMachine

My implementation for a State Machine. It can be used to implement and extend
simple command line tools.
The States can be moved to modules and assembled in the main file.
The Configuration can live also in the main file, so this would be the only
one which should be maintained.

TODO:
  - Clear the implementation
  - Check out how to implement multiple return choices (not only callback and errback)
  - Move to use with twisted reactor.
"""

import random
 
class StateMachine(object): 
 
    def __init__(self): 
        """Initialize the Machine with the Startstate.""" 
        self.currentState = None 
        self.startState = None 
        self.endStates = {}
        self.states = {}
    
    def addState(self, state, isStart=False, isEnd=False): 
        """Add a new State to states list.""" 
        self.states[state.name] = state
        
        if isStart:
            self.startState = state
        
        if isEnd:
            self.endStates[state.name] = state
    
    def setStart(self): 
        """Prepare everything."""
        if not self.startState:
            raise Exception("Startstate not set!")
        if not self.endStates:
            raise Exception("Endstate not set!")

        self.currentState = self.startState
     
    def render(self, input): 
        """Check input for the current state. 
        If input is valid, 
            - process State with input 
        """ 
        newState, data = currentState.process(request) 
        self.currentState = self.states[newState](data)               
    
    def run(self):        
        print "Starting MyMachine: \n"
        while True:
            input = raw_input("What you want: \n{state}".format(state=self.currentState.render()))
            print "Got input: ", input, " for State: ", self.currentState
            newState, data = self.currentState.process(input)
            print "RETURNED: ", newState, data
            if newState in self.endStates.keys():
                print "Yiiiiihhhhaaaa, Ready!"
                break
            else:
                self.currentState = self.states[newState]
                self.currentState.render()
        print "Bye"


class State(object):
         
    name = '' 
    acceptInput = {}
    actInput = ''
    
    def __init__(self, name, transition={}): 
        """Initialize state.""" 
        self.name = name 
        self.acceptInput = transition
    
    def __call__(self, input):
        print "{name} called with: {input}".format(name=self.name
                                                  ,input=self.input)
        self.data = input
    
    def render(self): 
        raise NotImplementedError()
    
    def process(self, input):
        raise NotImplementedError()
    
    def _validateInput(self, input):
        if input in self.acceptInput:
            return True
        return False


class StartState(State):
  
    def render(self):
        output = "Please give me some input:\n{input}".format(input = '\n'.join(self.acceptInput))
        output += "\n:"
        return output
    
    def process(self, input):
        self.actInput = input
        if self._validateInput(input):
            funcName = self.acceptInput[input]['action']
            print "FuncName: ", funcName
            func = getattr(self, funcName, None)
            print "Func: ", func
            return func()
        else:
            print "Not valid Input! \n"
            return self, self.data
    
    def do(self):
        print "do is on"
        rndNum = random.random()
        if rndNum <= 0.5:
            print "Return callback: ", self.acceptInput[self.actInput]['callback'], ''
            return (self.acceptInput[self.actInput]['callback'], '')
        else:
            print "Return errback: ", self.acceptInput[self.actInput]['errback'], ''
            return (self.acceptInput[self.actInput]['errback'], '')
    
    def da(self):
        print "da is on"
        rndNum = random.random()
        if rndNum <= 0.5:
            return (self.acceptInput[self.actInput]['callback'], '')
        else:
            return (self.acceptInput[self.actInput]['errback'], '')

class State2(State):
  
    def render(self):
        output = "Please give me some input:\n{input}".format(input = '\n'.join(self.acceptInput))
        output += "\n:"
        return output
    
    def process(self, input):
        self.actInput = input
        if self._validateInput(input):
            funcName = self.acceptInput[input]['action']
            func = getattr(self, funcName, None)
            return func()
        else:
            print "Not valid Input! \n"
            return self, self.data

    def do(self):
        print "do is on"
        rndNum = random.random()
        if rndNum <= 0.5:
            return self.acceptInput[self.actInput]['callback'], ''
        else:
            return self.acceptInput[self.actInput]['errback'], ''
    
    def da(self):
        print "da is on"
        rndNum = random.random()
        if rndNum <= 0.5:
            return self.acceptInput[self.actInput]['callback'], ''
        else:
            return self.acceptInput[self.actInput]['errback'], ''

class Success(State):
  
    def render(self):
        output = "Please give me some input:\n{input}".format(input = '\n'.join(self.acceptInput))
        output += "\n:"
        return output
    
    def process(self, input):
        if self._validateInput(input):
            funcName = self.acceptInput[input]['action']
            func = getattr(self, funcName, None)
            return func()
        else:
            print "Not valid Input! \n"
            return self, self.data
            

class ErrState(State):
  
    def render(self):
        output = "Please give me some input:\n{input}".format(input = '\n'.join(self.acceptInput))
        output += "\n:"
        return output
    
    def process(self, input):
        if self._validateInput(input):
            funcName = self.acceptInput[input]['action']
            func = getattr(self, funcName, None)
            return func()
        else:
            print "Not valid Input! \n"
            return self, self.data


if __name__ == "__main__": 
    start_state = StartState('start',
        {'weiter':{'action':'do', 'callback':'state2', 'errback':'start'}
        ,'abbruch':{'action':'da', 'callback':'error', 'errback':'error'}})
    state2 = State2('state2', 
        {'weiter':{'action':'do', 'callback':'success', 'errback':'state2'}
        ,'abbruch':{'action':'da', 'callback':'error', 'errback':'error'}})
    success = Success('success')
    error = ErrState('error')
    sm = StateMachine()
    sm.addState(start_state, isStart=True) 
    sm.addState(state2) 
    sm.addState(success, isEnd=True) 
    sm.addState(error, isEnd=True) 
    sm.setStart()
    sm.run()