from optparse import OptionParser
from github3 import login, GitHub
from getpass import getpass
from ConfigParser import ConfigParser
import os

__version__ = '0.1a'
__author__ = 'Ian Cordasco'

#: Dictionary holding the basic configuration for the script. By default the
#  script operates anonymously to view the issues of the projects listed. The
#  projects should be in the form ('owner', 'name') and will be read from both
#  the command line and configuration file.
config = {
        'anonymous': True,
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


def read_config(config='', username=''):
    """Read the configuration file.

    :param config: (optional), path to the configuration file to use,
        default: $HOME/.issuesrc
    :type config: str
    """
    config = config or os.path.join(os.environ['HOME'], '.issuesrc')
    parser = ConfigParser()
    with open(config, 'r') as fd:
        parser.readfp(fd, config)
        sections = parser.sections()

        # Get the authentication information
        if 'auth' in sections:
            sections.remove('auth')
            # Command-line options should override the config file
            if not username and parser.has_option('auth', 'username'):
                config['username'] = parser.get('auth', 'username')
            elif username:
                config['username'] = username

            # In case someone doesn't like putting their password in 
            # plain-text into a file on their computer (which I 
            # **completely**) understand.
            if parser.has_option('auth', 'password'):
                config['password'] = parser.get('auth', 'password')

            # Check for oauth token
            if parser.has_option('auth', 'oauth'):
                config['oauth'] = parser.get('auth', 'oauth')

        if config['username']:
            config['anonymous'] = False

        # If we only have half of the authorization...
        if config['username'] and not config['password']:
            fs = 'Password for {0}: '.format(config['username'])
            # Be persistent
            while not config['password']:
                config['password'] = getpass(fs)

        for sect in sections:
            projects = [(sect, proj) for (proj, _) in parser.items(sect)]
            config['projects'].extend(projects)


def list_all():
    """List every open issue on every project desired"""
    pass


def main():
    opts = initialize_opts()
    (valid, args) = opts.parse_args()
    read_config(valid.conf)

    # Setup our GitHub object
    if (config['username'] and config['password']) or config['oauth']:
        config['github'] = login(config['username'], config['password'], 
                config['oauth'])
    else:
        config['github'] = GitHub()

    # If no command was issues, let's simply list everything
    if not args:
        list_all()
