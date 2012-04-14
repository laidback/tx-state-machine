State Machine
=============

Python State Machine für die Benutzung als Basis für Consolen Programme für die Administration

TODO:
-----

- Cleanup the implementation
- Check out how to implement multiple return choices (not only callback and errback)
- Move State(s) to own files
- Implement to work with twisted reactor
- Implement to use with Webserver
	- Save in Session
	- Load from Session
- Implement in Yii and as Extension for Typo3
- Implement for Django

See:
----

http://en.wikipedia.org/wiki/Finite_state_machine#Mathematical_model

Usage:
------

>>> # Create States from Implementations derived from 'State'
>>> # params are: name, event with action and the resulting new State
>>> start_state = StartState('start',
	{'go': {'action': 'doSomething', 'callback': 'state2', 'errback': 'start'}
	,'cancel': {'action': 'doOtherThing', 'callback': 'error', 'errback': 'error'}})
>>> state2 = StartState('state2',
	{'go': {'action': 'doSomething', 'callback': 'success', 'errback': 'state2'}
	,'cancel': {'action': 'doOtherThing', 'callback': 'error', 'errback': 'error'}})
>>> success = Success('success')
>>> error = ErrState('error')
>>> 
>>> # Create State Machine and add some States
>>> stateMachine = StateMachine()
>>> stateMachine.addState(start_state, isStart=True)
>>> stateMachine.addState(state2)
>>> stateMachine.addState(success, isEnd=True)
>>> stateMachine.addState(error, isEnd=True)
>>> stateMachine.setStart()
>>> stateMachine.run()


