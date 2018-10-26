receives
========

**receives** is an mocking library to make general mocking in tests more easy
and better readable.

Features of **receives** are:

   * Easy to use syntax (on method rules them all)
   * Class based mocking (no access to underlying instances required)
   * Automatic call counting
   * Validate method arguments

Quick example
-------------

.. code-block:: python

   from receives import receives

   class Stack():
      def __init__(self):
         self._data = []

      def push(self, value):
         self._data.append(value)
         return value

      def pop(self):
         return self._data.pop()

   @receives
   def test_stack_push(receive):
      receive(Stack, "push").with_args(42).and_return(4)

      stack = Stack()
      assert(stack.push(42) == 4)


Installation
------------

to install **receives** use `pip`:

.. code-block:: bash

   $ pip install receives

for more information checkout :ref:`install-instructions`.


Bugs and feedback
-----------------

You found a bug or you want some features added? No problem go to
`Github issues <https://github.com/felixsch/receives/issues>`_ and create
a new issue.

Contents
========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   mocks
   expectations



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
