*****
Usage
*****

This project produces both a command line tool and a Python library with usable public APIs.

.. contents::
    :depth: 1
    :backlinks: top
    :local:

Prerequisites
=============

* Python 3.4+
* A MacOS or Unix-like operating system.
* Installation of this package, ``rudi-dire-insp``, in your local runtime environment (virtualenv etc.).

Command Line
============

A single command line tool is provided, below is an example of invoking it with the ``--help`` option::

    > rudi-dire-insp --help
    usage: rudi-dire-insp [-h] [--verbose | --debug] [--output OUTPUT_PATH] input_path

    Rudimentary directory inspector

    positional arguments:
      input_path            The directory to inspect

    optional arguments:
      -h, --help            show this help message and exit
      --verbose, -v         Set log level to INFO
      --debug, -d           Set log level to DEBUG
      --output OUTPUT_PATH, -o OUTPUT_PATH
                            Output path for the inspection results


Inputs
------

* The value for the ``input_path`` argument needs to be a path to a valid directory.

Outputs
-------

* If the ``--output`` option is not used, then the tool will output to ``STDOUT``.
* Regardless of where the output goes, the tools will always log to ``STDERR``.

The standard output consists of multiple lines of text, where each one is a single serialized JSON object.

Below is the JSON Schema for each of those JSON objects:

.. literalinclude:: ../tests/integration/data/output-schema.json
    :language: javascript

As a Library
============

This package can be imported into your Python project as follows:

.. code-block:: python

    import rudi_dire_insp

For more detailed information on its public APIs, please see the :ref:`api-docs` chapter.
