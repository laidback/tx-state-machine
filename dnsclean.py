#!/usr/env python
# -*- coding: utf-8 *-*

# Copyright (c) Former03 GmbH
# See LICENSE for details.


"""txStateMachine
Reads commands from the stdin and returns results.
"""
from twisted.internet import stdio, reactor
from twisted.protocols import basic

from os import linesep
from config import states, startState, endStates


class Echo(basic.LineReceiver):

    delimiter = linesep
    currentState = None
    startState = None
    endStates = {} 
    sharedData = {}
    states = {}

    def makeConnection(self, transport):
        print "making Connection..."
        self.currentState = self.getInitialState()
        basic.LineReceiver.makeConnection(self, transport)

    def connectionMade(self):
        self.transport.write(self.startState.render())

    def lineReceived(self, line):
        # ignore blank lines.
        if not line: return        
        
        # go out if the user wants us to.
        if line in ('exit', 'quit', 'aus', 'off'):
            self.endSession()
        else:
            nextState, data = self.currentState.process(line)
            self.currentState = self.states.get(nextState)(data)
            print self.endStates.keys(), nextState
            if nextState in self.endStates.keys():
                self.sendLine(self.currentState.render())                
                self.endSession()
            else:            
                self.transport.write(self.currentState.render())

    def getInitialState(self):
        if not self.startState:
            raise NotImplemented("startState is missing")
        return self.startState
    
    def endSession(self):
        self.sendLine('Goodbye!')
        self.transport.loseConnection()
    
    def addStates(self, states):
        for name, state in states.iteritems():
            self.addState(state)

    def addState(self, state):
        self.states[state.name] = state

        if state.isStart:
            if self.startState is not None:
                raise NotImplemented("Self startnode already exists!")
            else:
                self.startState = state
         
        if state.isEnd:
            self.endStates[state.name] = state

    def setStart(self, state):
        if self.startState is not None:
            raise NotImplemented("Startnode already set!")
        self.startState = state

    def setEndStates(self, endStates):
        self.endStates = endStates

    def connectionLost(self, reason):
        # stop the reactor, only because this is meant to be run in Stdio.
        reactor.stop()

def main():
    try:
        stateMachine = Echo()
        stateMachine.addStates(states)
    except Exception, e:
        print "Some error occured: {err}".format(err=e.getErrorMessage())
        sys.exit("Quitting due to error in programming")
    stdio.StandardIO(stateMachine)
    reactor.run()

if __name__ == '__main__':
    main()
