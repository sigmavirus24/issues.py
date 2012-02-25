# GitHub Issues Python Mananger

In the vein of [todo.py](http://git.io/todo.py)

The project is meant to be a standalone script like
[todo.py](http://git.io/todo.py) but can be used as a module presently and
in the future as well probably. It works on Python 2.6-3.x.

# Dependencies

I could have used Kenneth Reitz's great
[requests](https://github.com/kennethreitz/requests) module for this, but I
wanted to have as few dependencies as possible. If someone else wants to do
this using his module, they fork this and integrate that.

# Module Example 

```python
from issues import Issues

i = Issues(owner='sigmavirus24', project='Todo.txt-python')
i.fetch_issues(check_cache=True, cache_dir='.')
i.print_issues()
i.cache('.')
```

This will check the current directory for a cache file of the project, if
it's not there, it will go to the GitHub API (v3) to get it. After printing
the issues in numerical order, it will then cache them in the current
directory. I don't know about you, but that's pretty clean and concise if
you ask me.

You can also get your own issues like so:

```python
from issues import Issues

i = Issues(user='sigmavirus24', pw='not_my_real_password')
i.fetch_issues(check_cache=True, cache_dir='.')
i.print_issues()
i.cache('.')
```
