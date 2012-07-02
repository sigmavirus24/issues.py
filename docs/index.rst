issues.py
=========

A simple python script to monitor yours (and other people's) issues on GitHub_ 
projects. Most of the heavy lifting is done by github3.py_ -- a Python wrapper 
for the GitHub API v3.

Installation
------------

::

    $ pip install issues.py

Or:

::

    $ git clone git://github.com/sigmavirus24/issues.py.git
    $ cd issues.py
    $ python setup.py install

Configuration
-------------

In your ``$HOME`` directory, start a file called ``.issuesrc``. The file uses 
json to organize the information in a sensible and logical way.

======== ==================
Param    Explanation
======== ==================
auth     authentication parameters
projects projects you're watching
options  script options
======== ==================

.. links
.. _GitHub: https://github.com
.. _github3.py: http://github3py.rtfd.org
