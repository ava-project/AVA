# AVA
Desktop client for the AVA vocal assistant.

## Installation

To write

## Organization

#### Components architecture
The AVA core is an orchestration of a bunch of components, all responsible of a single concern. These components are executed in different threads, and communicating from one to another by using `queue.Queue` from the Python standard library. Components have a loose coupling and a tight cohesion, which mean they are not directly connected but use a well defined protocol. Each component is a class extending [_BaseComponents](ava/components.py) and must implement a `run` method. They may implement a `setup` method that will be called after the `__init__` and before the `run`. The method `run` of the component is by default executed in an infinite loop. This allow the component to have a very straight forward approach: execute a piece of code for one element popped out the queue. Some components might want to implement they own way to keep the thread alive: the component must inherit the class `RunOneTime` from [ava/components.py](ava/components.py).

#### Threading components
The components should not thread themselves. They should respond to a single concern. The main thread of the AVA Core is responsible of creating all the required threads and instantiate the component in it. The [ComponentManager](ava/components.py) is the class responsible of it. The API is simple, `add_component` adds a component to the list, `start_all` instantiate and run all the components in a thread fashion.

#### Queues
The queues are singleton objects, each component can freely get the instance of a queue and send messages. All the queues are defined in [ava/queues.py](ava/queues.py). A queue should have a single purpose, and only one consumer. Multiple components can write in a queue, but only one can read from it. Most of components passively read from that queue, and react when data arrives.

## Components

#### Speech to Text

The [Speech to Text](ava/speech_to_text) is responsible to convert the speech to a text format. It listens the chosen input (raw from the computer or through mobile app), then translate it into a string, and sends that string to the `QueueCommand` queue.

#### Executor

The [Executor](ava/executor) is responsible to analyze the command of the user and dispatch the action to the right component. It listens to the `QueueCommand` queue and write to :
 - `QueuePlugin` if the command is an action for the plugin manager

#### Plugin manager

The [Plugin manager](ava/plugin_manager) is responsible to install, configure and forward commands to the plugins. It listens to the `QueuePlugin` queue for incoming command, then selections the right plugin to execute it. The result of the command can be communicate to the Text to Speech component by writing it to the `QueueTtS` queue.

#### Text to Speech

The [Text to Speech](ava/text_to_speech) gives a vocal response to the user. It listen to the `QueueTtS` for incoming text to read.
