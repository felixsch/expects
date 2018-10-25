Usage
=====

Initialization
--------------

**receives** is initialized using the `receives` decorator to enable mocking
methods.

.. automodule:: receives.receiver
   :members:
   :inherited-members:
   :no-special-members:

The decorator injects the `receive object` as additional argument to your test method.
New mocks are defined by calling the `receive` object.

.. function:: receive(object, "method")

   Mock a `method` from given `object`.

   **Args**:
      `object`   An instance, class or module which owns the method
      `method`   Name of the method to mock

   **Returns** a newly created Expectation

.. code-block:: python

   from receives import receives

   from mylib import MyClass


   @receives
   def test_a_method(receive):
      receive(MyClass, "method").with_args("python rules").and_return("maybe")

      myclass = MyClass()
      assert(myclass.method("python rules") == "maybe")

Call count recording
--------------------

**receives** records how often a mocked method_a is called during the test. If you
add **one** mock for **method_a** and **method_a** is called twice the test will fail.

.. code-block:: python

   from receives import receives

   class Test():
      def method_a(self):
         return 42

   @receives
   def test_method_a(receive):
      receive(Test, "method_a").and_return(1)
      receive(Test, "method_a").and_return(1)

      t = Test()

      t.method_a()
      t.method_a()
      t.method_a()
      t.method_a()
      t.method_a()

   # E AssertionError: Expected Test.method_a to run 2 times but run 5 times.

Expectations
------------

Most importantly are general expectations you can define for each mock.
the `receive object` returns a new created `Exceptation` which is used to define
your expectations to the mocked call.

For example, if the mocked call should receive `"tim"` as argument:

.. code-block:: python

   from receives import receives

   from mylib import MyClass


   @receives
   def test_myclass_method(receive):
      myclass = MyClass()

      receive(myclass, "method").with_args("tim")

      myclass.method("tom")

      # E AssertionError: myclass.method received unexpected arguments:
      # E expected:
      # E   ('tim',)
      # E got instead:
      # E   ('tom',)

for more information what expectations can be defined goto :ref:`Expectations`.
