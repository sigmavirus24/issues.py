#!/usr/bin/env python

from optparse import OptionParser
from github3 import login, GitHub
from getpass import getpass
import sys
import json
import os

__version__ = '0.0a'
__author__ = 'Ian Cordasco'

#: Dictionary holding the basic configuration for the script. By default the
#  script operates anonymously to view the issues of the projects listed. The
#  projects should be in the form ('owner', 'name') and will be read from both
#  the command line and configuration file.
config = {
        'username': '',
        'password': '',
        'oauth': '',
        'projects': [],
        'github': None,
        }


# I'm using this from todo.py (http://git.io/todo.py) because it gets the job 
# done
def usage(*args):
    """Set the usage string printed out in help."""
    def usage_decorator(func):
        """Function that actually sets the usage string."""
        func.__usage__ = '\n'.join(args).expandtabs(3)
        return func
    return usage_decorator


def format_issue(issue):
    """Format an issue for printing

    :param issue: (required), issue to parse
    :type issue: :class:`packages.github3.issue.Issue`
    :returns str:
    """
    # format string
    fs = '[#{i.number}] {i.title:.18} - @{u.login} ({r[0]}/{r[1]})'
    return fs.format(i=issue, u=issue.user, r=issue.repository)


def get_issue(args):
    """Handle the cases for retrieving a single issue.

    :param args: should be a tuple, e.g., ('owner', 'repo', 'number'),
        ('owner/repo', 'number'), ('repo', 'number), or even
        ('owner/repo#number')
    :returns: :class:`Issue <github3.issue.Issue>`
    """
    proj = ()
    num = 0
    _get = config['github'].issue
    if any(args) and len(args) == 3:
        proj = (args[0], args[1])
        num = args[-1]
    elif any(args) and len(args) == 2:
        if '/' in arg[s0]:
            proj = args[0].split('/')
        elif config['username']:
            proj = (config['username'], args[0])
        num = args[-1]
    elif any(args) and len(args) == 1:
        if '#' in args[0]:
            (args, num) = args[0].split('#')
        if '/' in args:
            proj = args.split('/')
        elif config['username']:
            proj = (config['username'], args)

    if proj:
        return _get(proj[0], proj[1], num)
    return None


def initialize_opts():
    """Initialize the command-line options."""
    opts = OptionParser('Usage: %prog [options] actions [arg(s)]')
    #opts.remove_option('-h')
    #opts.add_option('-h', '--help', action='callback', callback=print_help)
    opts.add_option('-c', '--config', dest='conf', default='', type='string',
            nargs=1, help='Configuration file to read')
    opts.add_option('-u', '--username', dest='user', default='',
            type='string', nargs=1, help='Username to authenticate with')
    return opts


def read_config(config_file='', username=''):
    """Read the configuration file.

    :param config: (optional), path to the configuration file to use,
        default: $HOME/.issuesrc
    :type config: str
    """
    config_file = config_file or os.path.join(os.environ['HOME'], '.issuesrc')
    options = None
    if os.path.exists(config_file):
        with open(config_file, 'r') as fd:
            options = json.load(fd)

    if not options:
        return

    auth = options.get('auth', {})
    config.update(auth)

    projs = options.get('projects', {})
    for (k, v) in projs.items():
        projs = [(k, p) for p in v]
        config['projects'].extend(projs)


### Commands
@usage('\tlistall | lsa', '\t\t' +\
        'List every open issue on every project listed in the config file\n')
def list_all(args):
    """List every open issue on every project desired"""
    if not any(config['projects']):
        return

    if args:
        return

    for (owner, project) in config['projects']:
        print('----{0}/{1}:'.format(owner, project))
        for issue in config['github'].list_issues(owner, project):
            print(format_issue(issue))

@usage('\tlistcomments | lsco owner repo issue',
        '\t\tList comments on :owner/:repo#:issue.\n')
def list_comments(args):
    """List comments on an issue.

    :param args: owner, repo, number
    :type args: list
    """
    args = args or ()
    issue = get_issue(args)

    comments = issue.list_comments()

    fs = '@{0}:------------'
    for c in comments:
        print(fs.format(c.user.login))
        print(c.body)


@usage('\tmore | info owner repo issue',
        '\t\tRetrieve more information about the issue\n')
def more_info(args):
    """Get more information about a particular issue on a repository.

    :param args: owner, repo, number
    :type args: list
    """
    args = args or ()
    issue = get_issue(args)
    if issue:
        print(format_issue(issue))
        print(issue.body)


@usage('\thelp', '\t\tPrint this message\n')
def print_help(*args):
    """Function triggered by 'help' and '-h/--help'."""
    print('Usage: {0} [options] [command [args]]\n'.format(sys.argv[0]))
    visited = []
    for key in sorted(commands.keys()):
        func = commands[key]
        if func not in visited:
            print(func.__usage__)
            visited.append(func)
    sys.exit(0)
### End Commands


def main():
    opts = initialize_opts()
    (valid, args) = opts.parse_args()
    read_config(valid.conf, valid.user)

    # Setup our GitHub object
    if (config['username'] and config['password']) or config['oauth']:
        config['github'] = login(config['username'], config['password'], 
                config['oauth'])
    elif config['username'] and not config['password']:
        while not config['password']:
            pass_str = 'Password for {0}: '.format(config['username'])
            config['password'] = getpass(pass_str)
        config['github'] = login(config['username'], config['password'])
    else:
        config['github'] = GitHub()

    # If no command was issues, let's simply list everything
    if not args:
        list_all()
        return

    command = args.pop(0)
    if command in commands:
        commands[command](args)


commands = {
        'more': more_info,
        'info': more_info,
        'listcomments': list_comments,
        'lscm': list_comments,
        #'comment': comment,
        'help': print_help,
        }


if __name__ == '__main__':
    main()
