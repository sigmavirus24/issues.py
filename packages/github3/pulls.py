"""
github3.pulls
=============

This module contains all the classes relating to pull requests.

"""

from json import dumps
from .git import Commit
from .models import GitHubCore, BaseComment
from .user import User


class PullDestination(GitHubCore):
    """The :class:`PullDestination <PullDestination>` object."""
    def __init__(self, dest, direction):
        super(PullDestination, self).__init__(None)
        self._dir = direction
        self._ref = dest.get('ref')
        self._label = dest.get('label')
        self._user = None
        if dest.get('user'):
            self._user = User(dest.get('user'), None)
        self._sha = dest.get('sha')
        self._repo_name = ''
        self._repo_owner = ''
        if dest.get('repo'):
            self._repo_name = dest['repo'].get('name')
            self._repo_owner = dest['repo']['owner'].get('login')

    def __repr__(self):
        return '<%s [%s]>' % (self._dir, self._label)

    @property
    def label(self):
        """label of the destination"""
        return self._label

    @property
    def sha(self):
        """SHA of the commit at the head"""
        return self._sha

    @property
    def ref(self):
        """Full reference string of the object"""
        return self._ref

    @property
    def repo(self):
        """(owner, name) representing the repository this is on"""
        return (self._repo_owner, self._repo_name)

    @property
    def user(self):
        """:class:`User <user.User>` representing the owner"""
        return self._user


class PullFile(object):
    """The :class:`PullFile <PullFile>` object."""
    def __init__(self, pfile):
        super(PullFile, self).__init__()
        self._sha = pfile.get('sha')
        self._name = pfile.get('filename')
        self._status = pfile.get('status')
        self._add = pfile.get('additions')
        self._del = pfile.get('deletions')
        self._changes = pfile.get('changes')
        self._blob = pfile.get('blob_url')
        self._raw = pfile.get('raw_url')
        self._patch = pfile.get('patch')

    def __repr__(self):
        return '<Pull Request File [%s]>' % self._name

    @property
    def additions(self):
        """Number of additions on this file"""
        return self._add

    @property
    def blob_url(self):
        """URL to view the blob for this file"""
        return self._blob

    @property
    def changes(self):
        """Number of changes made to this file"""
        return self._changes

    @property
    def deletions(self):
        """Number of deletions on this file"""
        return self._del

    @property
    def filename(self):
        """Name of the file"""
        return self._name

    @property
    def patch(self):
        """URL to view the patch"""
        return self._patch

    @property
    def raw_url(self):
        """URL to view the raw diff of this file"""
        return self._raw

    @property
    def sha(self):
        """SHA of the commit"""
        return self._sha

    @property
    def status(self):
        """Status of the file, e.g., 'added'"""
        return self._status


class PullRequest(GitHubCore):
    """The :class:`PullRequest <PullRequest>` object."""
    def __init__(self, pull, session):
        super(PullRequest, self).__init__(session)
        self._update_(pull)

    def __repr__(self):
        return '<Pull Request [#%d]>' % self._num

    def _update_(self, pull):
        self._api = pull.get('url')
        self._base = PullDestination(pull.get('base'), 'Base')
        self._body = pull.get('body')

        self._closed = None
        # If the pull request has been closed
        if pull.get('closed_at'):
            self._closed = self._strptime(pull.get('closed_at'))

        self._created = self._strptime(pull.get('created_at'))
        self._diff = pull.get('diff_url')
        self._head = PullDestination(pull.get('head'), 'Head')
        self._url = pull.get('html_url')
        self._id = pull.get('id')
        self._issue = pull.get('issue_url')

        # These are the links provided by the dictionary in the json called
        # '_links'. It's structure is horrific, so to make this look a lot
        # cleaner, I reconstructed what the links would be:
        #  - ``self`` is just the api url, e.g.,
        #    https://api.github.com/repos/:user/:repo/pulls/:number
        #  - ``comments`` is just the api url for comments on the issue, e.g.,
        #    https://api.github.com/repos/:user/:repo/issues/:number/comments
        #  - ``issue`` is the api url for the issue, e.g.,
        #    https://api.github.com/repos/:user/:repo/issues/:number
        #  - ``html`` is just the html_url attribute
        #  - ``review_comments`` is just the api url for the pull, e.g.,
        #    https://api.github.com/repos/:user/:repo/pulls/:number/comments
        self._links = {
                'self': self._api,
                'comments': '/'.join([self._api.replace('pulls', 'issues'),
                    'comments']),
                'issue': self._api.replace('pulls', 'issues'),
                'html': self._url,
                'review_comments': self._api + '/comments'
                }

        self._merged = None
        # If the pull request has been merged
        if pull.get('merged_at'):
            self._merged = self._strptime(pull.get('merged_at'))
        self._mergeable = pull.get('mergeable')
        self._mergedby = None
        if pull.get('merged_by'):
            self._mergedby = User(pull.get('merged_by'), self._session)
        self._num = pull.get('number')
        self._patch_url = pull.get('patch_url')
        self._state = pull.get('state')
        self._title = pull.get('title')
        self._updated = self._strptime(pull.get('updated_at'))
        self._user = None
        if pull.get('user'):
            self._user = User(pull.get('user'), self._session)

    @property
    def base(self):
        """Base of the merge"""
        return self._base

    @property
    def body(self):
        """Body of the pull request message"""
        return self._body

    @property
    def closed_at(self):
        """datetime object representing when the pull was closed"""
        return self._closed

    @property
    def created_at(self):
        """datetime object representing when the pull was created"""
        return self._created

    @property
    def diff_url(self):
        """URL to view the diff associated with the pull"""
        return self._diff

    @property
    def head(self):
        """The new head after the pull request"""
        return self._head

    @property
    def html_url(self):
        """The URL of the pull request"""
        return self._url

    @property
    def id(self):
        """The unique id of the pull request"""
        return self._id

    def is_mergeable(self):
        """Checks to see if the pull request can be merged by GitHub.

        :returns: bool
        """
        return self._mergeable

    def is_merged(self):
        """Checks to see if the pull request was merged.

        :returns: bool
        """
        url = self._api + '/merge'
        return self._session.get(url).status_code == 204

    @property
    def issue_url(self):
        """The URL of the associated issue"""
        return self._issue

    @property
    def links(self):
        """Dictionary of _links"""
        return self._links

    def list_comments(self):
        """List the comments on this pull request.
        
        :returns: list of :class:`ReviewComment <ReviewComment>`\ s
        """
        url = self._api + '/comments'
        resp = self._get(url)
        ses = self._session
        return [ReviewComment(comment, ses) for comment in json]

    def list_commits(self):
        """List the commits on this pull request.
        
        :returns: list of :class:`Commit <github3.git.Commit>`\ s
        """
        url = self._api + '/commits'
        json = self._get(url)
        ses = self._session
        return [Commit(commit, ses) for commit in json]

    def list_files(self):
        """List the files associated with this pull request.
        
        :returns: list of :class:`PullFile <PullFile>`\ s
        """
        url = self._api + '/files'
        json = self._get(url)
        return [PullFile(f) for f in json]

    def merge(self, commit_message=''):
        """Merge this pull request.

        :param commit_message: (optional), message to be used for the merge
            commit
        :type commit_message: str
        :returns: bool
        """
        data = {'commit_message': commit_message} if commit_message else None
        url = self._api + '/merge'
        resp = self._put(url, data)
        if resp.status_code == 200:
            return resp.json['merged']
        return resp.json['merged']

    @property
    def merged_at(self):
        """datetime object representing when the pull was merged"""
        return self._merged

    @property
    def merged_by(self):
        """:class:`User <github3.user.User>` who merged this pull"""
        return self._mergedby

    @property
    def number(self):
        """Number of the pull/issue on the repository"""
        return self._num

    @property
    def patch_url(self):
        """The URL of the patch"""
        return self._patch_url

    @property
    def state(self):
        """The state of the pull"""
        return self._state

    @property
    def title(self):
        """The title of the request"""
        return self._title

    def update(self, title='', body='', state=''):
        """Update this pull request.

        :param title: (optional), title of the pull
        :type title: str
        :param body: (optional), body of the pull request
        :type body: str
        :param state: (optional), ('open', 'closed')
        :type state: str
        :returns: bool
        """
        data = dumps({'title': title, 'body': body, 'state': state})
        json = self._patch(self._api, data)
        if json:
            self._update_(json)
            return True
        return False

    @property
    def user(self):
        """:class:`User <github3.user.User>` object representing the creator of
        the pull request"""
        return self._user


class ReviewComment(BaseComment):
    """The :class:`ReviewComment <ReviewComment>` object. This is used to
    represent comments on pull requests.
    """
    def __init__(self, comment, session):
        super(ReviewComment, self).__init__(comment, session)

    def __repr__(self):
        return '<Review Comment [%s]>' % self._user.login

    @property
    def commit_id(self):
        """SHA of the commit the comment is on"""
        return self._cid
    
    @property
    def html_url(self):
        """URL of the comment"""
        return self._url

    @property
    def path(self):
        """Path to the file"""
        return self._path

    @property
    def position(self):
        """Position within the commit"""
        return self._pos

    @property
    def updated_at(self):
        """datetime object representing the last time the object was updated."""
        return self._updated
