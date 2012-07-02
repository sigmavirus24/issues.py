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
json to organize the information in a sensible and logical way. The three keys 
are described in the following table:

======== ==================
Param    Explanation
======== ==================
auth     authentication parameters
projects projects you're watching
options  script options
======== ==================

auth
~~~~

The auth section is a dictionary with three (straightforward) possible 
parameters:

- username
- password
- oath

If you're uncomfortable providing your password in plain-text, you can either 
use OAuth to login or you can enter your username and allow the script to 
prompt you each and every time you want to get issues.

You may also entirely omit this section to track issues anonymously, just keep 
in mind that you won't be able to comment on or administer issues at all.

projects
~~~~~~~~

This is a dictionary where the key is the owner of the repository, and the 
value is a list of their repositories.

options
~~~~~~~

This is another dictionary that accepts the following keys:

========== ==========
Key        Value
========== ==========
filter     ("assigned", "created", "mentioned", "subscribed") [#]_
state      ("open", "closed") [#]_
labels     e.g. "bug,ui,@high"
sort       ("created", "updated", "comments") [#]_
direction  ("asc", "desc") [#]_
since      ISO8601 formatted string [#]_
========== ==========

.. [#] The default (set by the GitHub API) is "assigned"
.. [#] The default is "open"
.. [#] The default is "created"
.. [#] The default is "desc"
.. [#] An example would be "2012-07-02T18:39:03Z"

A Sample Config File
~~~~~~~~~~~~~~~~~~~~

::

    {
        "auth": {
            "username": "sigmavirus24"
        },
        "projects": {
            "sigmavirus24": [
                "Todo.txt-python",
                "github3.py",
                "issues.py",
                "sprunge.py"
            ],
            "kennethreitz": [
                "requests",
                "args",
                "clint"
            ]
        }
    }

.. links
.. _GitHub: https://github.com
.. _github3.py: http://github3py.rtfd.org
