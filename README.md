# GitHub Issues Python Mananger

In the vein of [todo.py](http://git.io/todo.py)

The project is meant to be a standalone script like
[todo.py](http://git.io/todo.py) but can be used as a module presently and
in the future as well probably. It works on Python 2.6-3.x.

# Dependencies

None.

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

## Example Output

**example_script.py**

```python
#!/usr/bin/env python

from issues import Issues

if __name__ == "__main__":
    i = Issues(owner='kennethreitz', project='clint')
    i.fetch_issues(check_cache=True, cache_dir='.')
    i.print_issues()
    i.cache('.')
```

```shell
sigma@virus:~/sandbox/issues.py$ example_script.py 
  2 clint.textui.maxwidth context manager (kennethreitz) +Feature Request 
  3 clint.resources.bundler (kennethreitz) +Feature Request 
  4 256-color terminal support (laanwj) +Feature Request #{v0.2.4 - 2011-04-11T07:00:00Z}
  8 examples/text_width.py only works with terminals wider than 135 chars (redtoad) 
 10 Add underline support (kennethreitz) +Feature Request 
 11 wrap stdout.isatty in try/except (kennethreitz) 
 13 textui.auto_columns (kennethreitz) @kennethreitz #{v0.2.4 - 2011-04-11T07:00:00Z}
 15 Documentation (kennethreitz) 
 16 Background Color Support (kennethreitz) 
 17 Underline Color Support (kennethreitz) 
 19 added simple user input system (hunterlang) 
 23 added colors to progress bar and progress dots (jjanyan) 
 25 Make the width argument take into account the entire BAR_TEMPLATE, not j... (SirScott) 
 28 clint breaks readline completion (jandd) 
 33 data files installed in the wrong location (hannosch) 
 35 Fix for #33 - unwanted installation of data files. (hannosch) 
 36 Show details during a progress (GMLudo) 
 38 Try a reimplementation of clint.textui.core (Lothiraldan) 
 39 Windows colored text is not working (AltReality) 
 42 Initialise colorama for textui on Windows. (takluyver) 
 44 Fixed a typo in README.rst (mjs2600) 
```
