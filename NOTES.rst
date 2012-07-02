Configuration Management
========================

The configuration file will be managed by python's ConfigParser module. Because
of this decision, it should basically break down into two sections (more can be
added later):

- Authentication
- Projects

Authentication
--------------

The authentication section should look like this:

::

    [Authentication]
    user = sigmavirus24
    pass = fakepassword1234567890

Projects
--------

Because each 'option' can only have one value (which makes sense to be honest),
there needs to be a way to manage the projects that are being watched. My first
thought would be to do something like:

::

    [Projects]
    Todo.txt-python = sigmavirus24
    issues.py = sigmavirus24
    clint = kennethreitz
    fabric = fabric

The problem with this is, what if there exists a fork of one of the projects
which for whatever reason has its own issue tracker? Then you would have one 
option with multiple values. Ideally no fork has it's own issue tracker, but
it is certainly possible. Because of this possibility, I think there are two
possible ways of managing the configuration file. The first is to use the
repo owner as the section and list the projects you want to follow in that
section or to use the project as the section and list the owners whose
projects share that name under the section. I personally like the first, so
I'm going to write it so that the following is a valid configuration file:

::

    [Authentication]
    user = sigmavirus24
    pass = fakepassword1234567890
    
    [sigmavirus24]
    Todo.txt-python = 1
    issues.py = 1
    github3.py = 1
    
    [kennethreitz]
    clint = 1
    requests = 1
    httpbin = 1
    
    [fabric]
    fabric = 1

It's clean and more obvious in my humble opinion.
