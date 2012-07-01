from optparse import OptionParser
from github3 import login, GitHub

__version__ = '0.1a'
__author__ = 'Ian Cordasco'

def format_issue(issue):
    """Format an issue for printing

    :param issue: (required), issue to parse
    :type issue: :class:`packages.github3.issue.Issue`
    :returns str:
    """
    # format string
    fs = '[#{i.number}] {i.title:.18} - @{u.login} ({r[0]}/{r[1]})'
    return fs.format(i=issue, u=issue.user, r=issue.repository)
