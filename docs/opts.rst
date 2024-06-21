.. _opts:

:mod:`ipos.opts` --- Command-line options
=========================================

One of the basic ideas behind the global structure of the package is to have
a single `ipose` application that execute all the necessary tasks by a suitable
command-dispatch mechanism (implemented through `argparse` sub-parser) and, at the
same time, a python module that allows to call the same tasks from within Python,
in a programmatic fashion, through the exact same interface---only this time through
keyword arguments.

This module includes at the top-level a dictionary driving the creation of the
main argument parser to be used from command line, and the basic interfaces
(:meth:`default_value` and :meth:`default_kwargs`) to get the default values.


Module documentation
--------------------

.. automodule:: ipose.opts
