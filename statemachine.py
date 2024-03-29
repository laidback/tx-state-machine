#!/usr/env python2.7
# -*- coding: utf-8 *-*

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
