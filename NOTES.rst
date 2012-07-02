Configuration Management
========================

The configuration file will be valid json so it can be read easily.

- Authentication
- Projects

Authentication
--------------

The authentication section should roughtly look like this:

::

    {
        "auth": {
            "username": "sigmavirus24",
            "password": "foobar_bogus",
        }
    }

If you don't want your password saved in plain-text, you can use do this:

::

    {
        "auth": {
            "username": "sigmavirus24"
        }
    }

and ``issues.py`` will prompt you for your password each time.

Or you can use OAuth (assuming you have a token):

::

    {
        "auth": {
            "oauth": "<secret-key>"
        }
    }

If you leave out ``"auth"`` altogether, you will be using the API anonymously 
and will not be able to administer issues or comment on theme.

Projects
--------

And projects should look like this

::

    {
        "projects": [
            {
                "sigmavirus24": [
                    "Todo.txt-python",
                    "github3.py",
                    "issues.py",
                    "sprunge.py"
                ]
            },
            {
                "kennethreitz": [
                    "requests",
                    "clint",
                    "args"
                ]
            }
        ]
    }

A Complete Config File Example
------------------------------

::

    {
        "auth": {
            "username": "sigmavirus24",
            "password": "foobar_bogus",
        },
        "projects": [
            {
                "sigmavirus24": [
                    "Todo.txt-python",
                    "github3.py",
                    "issues.py",
                    "sprunge.py"
                ]
            },
            {
                "kennethreitz": [
                    "requests",
                    "clint",
                    "args"
                ]
            }
        ]
    }
