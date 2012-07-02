#!/usr/bin/env python

from optparse import OptionParser
from github3 import login, GitHub
from getpass import getpass
import json
import os

__version__ = '0.1a'
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

def format_issue(issue):
    """Format an issue for printing

    :param issue: (required), issue to parse
    :type issue: :class:`packages.github3.issue.Issue`
    :returns str:
    """
    # format string
    fs = '[#{i.number}] {i.title:.18} - @{u.login} ({r[0]}/{r[1]})'
    return fs.format(i=issue, u=issue.user, r=issue.repository)


def initialize_opts():
    """Initialize the command-line options."""
    opts = OptionParser('Usage: %prog [options] actions [arg(s)]')
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
    with open(config_file, 'r') as fd:
        options = json.load(fd)

    if not options:
        return

    auth = options.get('auth', {})
    config.update(auth)

    projs = options.get('projects', [])
    for d in projs:
        for (k, v) in d.items():
            p = [(k, p) for p in v]
            config['projects'].extend(p)


def list_all():
    """List every open issue on every project desired"""
    if not any(config['projects']):
        return

    for (owner, project) in config['projects']:
        print('----{0}/{1}:'.format(owner, project))
        for issue in config['github'].list_issues(owner, project):
            print(format_issue(issue))
        print('----')


def main():
    opts = initialize_opts()
    (valid, args) = opts.parse_args()
    read_config(valid.conf, valid.user)

    # Setup our GitHub object
    if (config['username'] and config['password']) or config['oauth']:
        config['github'] = login(config['username'], config['password'], 
                config['oauth'])
    else:
        config['github'] = GitHub()

    # If no command was issues, let's simply list everything
    if not args:
        list_all()


if __name__ == '__main__':
    main()
