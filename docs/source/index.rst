.. Blue Interface documentation master file, created by
   sphinx-quickstart on Thu Mar  8 00:09:36 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Blue Interface API Documentation
==========================================

Blue Interface is a platform-agnostic Python API for controlling Blue robotic arms over a network connection.

It features:

- No dependency on ROS (or any particular version of Ubuntu)
- Easy connection to multiple robots
- Support for both Python 2 and 3
- Support for Mac, Windows, and Linux
- Support for Jupyter Notebooks

It's designed to be lightweight and easy-to-use! Sending a Blue "right" arm to its zero position, for example, is as simple as:

.. code-block:: python

   from blue_interface import BlueInterface

   blue = BlueInterface(side="right", ip="127.0.0.1")
   blue.set_joint_positions([0] * 7)

See Github_ for installation instructions and more usage examples.

.. _Github: https://github.com/berkeleyopenarms/blue_interface

.. .. toctree::
..    :maxdepth: 2
..    :caption: Contents:

----

.. automodule:: blue_interface
.. autoclass:: BlueInterface
   :members:
   :undoc-members:


.. Indices and tables
.. ==================
..
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
