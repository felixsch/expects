# receives
[![Build Status](https://travis-ci.org/felixsch/receives.svg?branch=master)](https://travis-ci.org/felixsch/receives) [![Coverage Status](https://coveralls.io/repos/github/felixsch/receives/badge.svg?branch=master)](https://coveralls.io/github/felixsch/receives?branch=master) [![GitHub license](https://img.shields.io/github/license/felixsch/receives.svg)](https://github.com/felixsch/receives) [![Read the docs](https://readthedocs.org/projects/receives/badge/?version=latest)]

**receives** is a easy to use mocking library for python 3 and python 2.7 to 
make testing more easy.

Documentation can be found at [Read the docs](https://receives.readthedocs.io/en/latest/).

```python

  from receives import receives
  from mylib import Stack


  @receives
  def test_stack(receive):
    stack = Stack()

    receive(stack, "push").with_args("Hello").and_call_original()
    receive(stack, "push").with_args("World").and_call_original()

    receive(stack, "pop").and_return("some value")
    receive(stack, "pop").and_call_original()

    stack.push("Hello")
    stack.push("World")

    assert(stack.pop() == "some value")
    assert(stack.pop() == "Hello")
    assert(stack.pop() == "World")

    # E AssertionError: Expected stack.pop to run 2 times but run 3 times.

```

## Installation

via pip:

  $ pip install receives

or via git:

  $ git clone https://github.com/felixsch/receives.git
  $ cd receives
  $ python setup.py install

## Issues & Features

Do you found a bug or you want to see a feature in **receives**?
Open a new GitHub issue!

## Development

To install **receives** in development mode:

  $ git clone https://github.com/felixsch/receives.git
  $ cd receives
  $ pip install -r devel-requirements.txt
  $ python setup.py develop

To run tests:

  $ cd receives
  $ tox


## Contribute

I love to hear from you. Fork the project and open a pull request! If you want
to make big changes, please contact me before to make sure the pull request gets
into master!

