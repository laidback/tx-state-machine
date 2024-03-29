#!/usr/env python
# -*- coding: utf-8 *-*

from states import *

start_state = StartState('start',
        {'weiter': {'action': 'do', 'callback': 'state2', 'errback': 'start'}
        ,'abbruch':{'action':'da', 'callback':'error', 'errback':'error'}})
state2 = State2('state2', 
    {'weiter':{'action':'do', 'callback':'success', 'errback':'state2'}
    ,'abbruch':{'action':'da', 'callback':'error', 'errback':'error'}})
success = Success('success')
error = ErrState('error')

states = {
	'start': start_state,
	'state2': state2,
	'success': success,
	'error': error
}
startState = start_state
endStates = {
	'success': success,
	'error': error
}
