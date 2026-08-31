"""Personal Finance Tracker package.

Groups the application modules:

* :mod:`tracker.models` -- the ``Transaction`` dataclass and domain constants.
* :mod:`tracker.inputs` -- validated terminal prompts.
* :mod:`tracker.cli` -- menus, formatting and the main loop.
* :mod:`tracker.charts` -- aggregation and matplotlib figures.

Persistence lives in the top-level :mod:`database` module.
"""
