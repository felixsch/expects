Mocking
=======

To support a variety of different use cases **receives** allows to mock `classes`,
`instances`, `properties` and `functions`.

To activate a mock on a method one of the :ref:`receivers` has to be used.


Mocking functions
-----------------

The easiest mocking style is to mock top level method (e.g. in modules):

.. code-block:: python

   # lib.py

   def say_hello_to(name):
      return "Hello, #{name}".format(name)

   # test_lib.py

   from receives import receives
   import lib

   @receives
   def test_say_hello_to(receive):
      receive(lib, "say_hello_to").with_args("Tom").and_return("Nope!")
      assert(lib.say_hello_to("Tom") == "Nope!")



Mocking class instances
-----------------------

To mock methods of `class instances` just use the same method as for :ref:`Mocking functions`
just replace the `module` with the **instance object**.

.. code-block:: python

   # lib.py

   class Greeter():
      greeting = "Hello, "

      def greet(self, name):
         return self.greeting + name

   # test_lib.py

   from receives import receives
   import lib

   @receives
   def test_greeter_greet(receive):
      greeter = lib.Greeter()
      receive(greeter, "greet").with_args("Holger").and_return("Hello, Felix")

      assert(greeter.greet("Holger") == "Hello, Felix")


Mocking classes
-----------------

Often enough its not possible to reach the class instance you want to mock. For
this there is `class based mocking`. This mock allows you do mock a method of an
instance which is not yet instanciated.


.. note::

   `Class` based mocks need to be inplace **before** mocking any instance of
   the same `class`!

.. code-block:: python

   # fifo.py

   class Fifo():
      def __init__(self):
         self._values = []

      def push(self, value):
         self._values.append(value)

      def pop(self):
         return self._values.pop(0)

   # communication.py

   import fifo

   class Communication():
      def __init__(self):
         self._queue = fifo.Fifo()

      def say(self, msg):
         self._queue.push(msg)

      def listen(self):
         return self._queue.pop()

   # test_communitcation.py

   from receives import receives

   from communication import Communication
   from fifo import Fifo


   @receives
   def test_communication_listen(receive):
      receive(Fifo, "pop").and_return("Hae?")
      receive(Fifo, "pop").and_return("I can't hear you!")

      comm = Communication()

      assert(comm.listen() == "Hae?")
      assert(comm.listen() == "I can't hear you!")


Mocking properties
------------------

Sometimes it can be useful to mock properties. **receives** detects automatically
if a `property` was mocked and acts accoringly. Since `properties` are created
at instanciation, it's **required to mock properties at class level**.

The implementation detects automatically if the `property` is readonly and generates
the mock accoringly.

Mocking special methods (e.g. `open`)
-------------------------------------

Currently **receives** does not support mocking special methods like `io.open`.
