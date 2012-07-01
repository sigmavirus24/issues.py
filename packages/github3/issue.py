"""
github3.issue
=============

This module contains the classes related to issues.

"""

from json import dumps
from re import match
from .models import GitHubCore, BaseComment
from .user import User


class Label(GitHubCore):
    """The :class:`Label <Label>` object. Succintly represents a label that
    exists in a repository."""
    def __init__(self, label, session):
        super(Label, self).__init__(session)
        self._update_(label)

    def __repr__(self):
        return '<Label [%s]>' % self._name

    def _update_(self, label):
        self._api = label.get('url')
        self._color = label.get('color')
        self._name = label.get('name')

    @property
    def color(self):
        """Color of the label, e.g., 626262"""
        return self._color

    def delete(self):
        """Delete this label.

        :returns: bool
        """
        return self._delete(self._api)

    @property
    def name(self):
        """Name of the label, e.g., 'bug'"""
        return self._name

    def update(self, name, color):
        """Update this label.

        :param name: (required), new name of the label
        :type name: str
        :param color: (required), color code, e.g., 626262, no leading '#'
        :type color: str
        :returns: bool
        """
        if color[0] == '#':
            color = color[1:]

        json = self._patch(self._api, dumps({'name': name,
            'color': color}))
        if json:
            self._update_(json)
            return True

        return False


class Milestone(GitHubCore):
    """The :class:`Milestone <Milestone>` object. This is a small class to
    handle information about milestones on repositories and issues.
    """
    def __init__(self, mile, session):
        super(Milestone, self).__init__(session)
        self._update_(mile)

    def __repr__(self):
        return '<Milestone [%s]>' % self._title

    def _update_(self, mile):
        self._api = mile.get('url')
        self._num = mile.get('number')
        self._state = mile.get('state')
        self._title = mile.get('title')
        self._desc = mile.get('description')
        self._creator = User(mile.get('creator'), self._session)
        self._open = mile.get('open_issues')
        self._closed = mile.get('closed_issues')
        self._created = self._strptime(mile.get('created_at'))
        self._due = None
        if mile.get('due_on'):
            self._due = self._strptime(mile.get('due_on'))

    @property
    def closed_issues(self):
        """The number of closed issues associated with this milestone."""
        return self._closed

    @property
    def created_at(self):
        """datetime object representing when the milestone was created."""
        return self._created

    @property
    def creator(self):
        """:class:`User <user.User>` object representing the creator of the
        milestone."""
        return self._creator

    def delete(self):
        """Delete this milestone.
        
        :returns: bool
        """
        return self._delete(self._api)

    @property
    def description(self):
        """Description of this milestone."""
        return self._desc

    @property
    def due_on(self):
        """datetime representing when this milestone is due."""
        return self._due

    def list_labels(self):
        """List the labels for every issue associated with this
        milestone.
        
        :returns: list of :class:`Label <Label>`\ s
        """
        url = self._api + '/labels'
        json = self._get(url)
        ses = self._session
        return [Label(label, ses) for label in json]

    @property
    def number(self):
        """Identifying number associated with milestone."""
        return self._num

    @property
    def open_issues(self):
        """Number of issues associated with this milestone which are still
        open."""
        return self._open

    @property
    def state(self):
        """State of the milestone, e.g., open or closed."""
        return self._state

    @property
    def title(self):
        """Title of the milestone, e.g., 0.2."""
        return self._title

    def update(self, title, state='', description='', due_on=''):
        """Update this milestone.

        state, description, and due_on are optional

        :param title: (required), new title of the milestone
        :type title: str
        :param state: (optional), ('open', 'closed')
        :type state: str
        :param description: (optional)
        :type description: str
        :param due_on: (optional), ISO 8601 time format: YYYY-MM-DDTHH:MM:SSZ
        :type due_on: str
        :returns: bool
        """
        inp = dumps({'title': title, 'state': state,
            'description': description, 'due_on': due_on})
        json = self._patch(self._api, inp)
        if json:
            self._update_(json)
            return True
        return False


class Issue(GitHubCore):
    """The :class:`Issue <Issue>` object. It structures and handles the data
    returned via the `Issues <http://developer.github.com/v3/issues>`_ section
    of the GitHub API.
    """
    def __init__(self, issue, session):
        super(Issue, self).__init__(session)
        self._update_(issue)

    def __repr__(self):
        return '<Issue [%s/%s #%s]>' % (self._repo[0], self._repo[1],
                self._num)

    def _update_(self, issue):
        if issue.get('assignee'):
            self._assign = User(issue.get('assignee'), self._session)
        self._body = issue.get('body')

        # If an issue is still open, this field will be None
        self._closed = None
        if issue.get('closed_at'):
            self._closed = self._strptime(issue.get('closed_at'))

        # Numer of comments
        self._comments = issue.get('comments')
        self._created = self._strptime(issue.get('created_at'))
        self._url = issue.get('html_url')
        self._id = issue.get('id')
        self._labels = [Label(l, self._session) for l in issue.get('labels')]

        # Don't want to pass a NoneType to Milestone.__init__()
        if issue.get('milestone'):
            self._mile = Milestone(issue.get('milestone'), self._session)
        self._num = issue.get('number')
        self._pull_req = issue.get('pull_request')
        m = match('https://github\.com/(\S+)/(\S+)/issues/\d+', self._url)
        self._repo = m.groups()
        self._state = issue.get('state')
        self._title = issue.get('title')
        self._updated = self._strptime(issue.get('updated_at'))
        self._api = issue.get('url')
        self._user = User(issue.get('user'), self._session)

    def add_labels(self, *args):
        """Add labels to this issue.

        :param args: (required), names of the labels you wish to add
        :type args: str
        :returns: bool
        """
        url = self._api + '/labels'
        json = self._post(url, dumps(list(args)), status_code=200)
        return True if json else False

    @property
    def assignee(self):
        """:class:`User <user.User>` representing the user the issue was assigned
        to."""
        return self._assign

    @property
    def body(self):
        """Body (description) of the issue."""
        return self._body

    def close(self):
        """Close this issue."""
        return self.edit(self._title, self._body, self._assign.login,
                'closed', self._mile, self._labels)

    @property
    def closed_at(self):
        """datetime object representing when the issue was closed."""
        return self._closed

    def comment(self, id_num):
        """Get a single comment by its id.

        The catch here is that id is NOT a simple number to obtain. If
        you were to look at the comments on issue #15 in
        sigmavirus24/Todo.txt-python, the first comment's id is 4150787.

        :param id_num: (required), comment id, see example above
        :type id_num: int
        :returns: :class:`IssueComment <IssueComment>`
        """
        json = None
        if int(id_num) > 0:  # Might as well check that it's positive
            url = '/'.join([self._github_url, self._repo[0],
                self._repo[1], 'issues', 'comments', str(id_num)])
            json = self._get(url)
        return IssueComment(json) if json else None

    @property
    def comments(self):
        """Number of comments on this issue."""
        return self._comments

    def create_comment(self, body):
        """Create a comment on this issue.
        
        :param body: (required), comment body
        :type body: str
        :returns: :class:`IssueComment <IssueComment>`
        """
        json = None
        if body:
            url = self._api + '/comments'
            json = self._post(url, dumps({'body': body}))
        return IssueComment(json, self._session) if json else None

    @property
    def created_at(self):
        """datetime object representing when the issue was created."""
        return self._created

    def edit(self, title=None, body=None, assignee=None, state=None,
            milestone=None, labels=[]):
        """Edit this issue.

        :param title: Title of the issue
        :type title: str
        :param body: markdown formatted body (description) of the issue
        :type body: str
        :param assignee: login name of user the issue should be assigned to
        :type assignee: str
        :param state: accepted values: ('open', 'closed')
        :type state: str
        :param milestone: the NUMBER (not title) of the milestone to assign
            this to [1]_
        :type milestone: int
        :param labels: list of labels to apply this to
        :type labels: list of str's
        :returns: bool

        .. [1] Milestone numbering starts at 1, i.e. the first milestone you
               create is 1, the second is 2, etc.
        """
        data = {'title': title, 'body': body, 'assignee': assignee,
                'state': state, 'milestone': milestone, 'labels': labels}
        json = self._patch(self._api, dumps(data))
        if json:
            self._update_(json)
            return True

        return False

    @property
    def html_url(self):
        """URL to view the issue at GitHub."""
        return self._url

    @property
    def id(self):
        """Unique ID for the comment."""
        return self._id

    def is_closed(self):
        """Checks if the issue is closed.
        
        :returns: bool
        """
        if self._closed or (self._state == 'closed'):
            return True
        return False

    @property
    def labels(self):
        """Returns the list of :class:`Label <Label>`\ s on this issue."""
        return self._labels

    def list_comments(self):
        """List comments on this issue.

        :returns: list of :class:`IssueComment <IssueComment>`
        """
        url = self._api + '/comments'
        json = self._get(url)
        ses = self._session
        return [IssueComment(comment, ses) for comment in json]

    def list_events(self):
        """List events associated with this issue only.

        :returns: list of :class:`IssueEvent <IssueEvent>`\ s
        """
        url = self._api + '/events'
        json = self._get(url)
        return [IssueEvent(event, self) for event in json]

    @property
    def milestone(self):
        """:class:`Milestone <Milestone>` this issue was assigned to."""
        return self._mile

    @property
    def number(self):
        """Issue number (e.g. #15)"""
        return self._num

    @property
    def pull_request(self):
        """Dictionary URLs for the pull request (if they exist)"""
        return self._pull_req

    def remove_label(self, name):
        """Removes label ``name`` from this issue.

        :param name: (required), name of the label to remove
        :type name: str
        :returns: bool
        """
        url = '{0}/labels/{1}'.format(self._api, name)
        return self._delete(url, status_code=200)

    def remove_all_labels(self):
        """Remove all labels from this issue.

        :returns: bool
        """
        # Can either send DELETE or [] to remove all labels
        return self.replace_labels([])

    def replace_labels(self, labels):
        """Replace all labels on this issue with ``labels``.

        :param labels: label names
        :type: list of str's
        :returns: bool
        """
        url = self._api + '/labels'
        return self._put(url, dumps(labels), status_code=200)

    def reopen(self):
        """Re-open a closed issue.

        :returns: bool
        """
        return self.edit(self._title, self._body, self._assign.login,
                'open', self._mile, self._labels)

    @property
    def repository(self):
        """:class:`Repository <repo.Repository>` this issue was filed on."""
        return self._repo

    @property
    def state(self):
        """State of the issue, e.g., open, closed"""
        return self._state

    @property
    def title(self):
        """Title of the issue."""
        return self._title

    @property
    def updated_at(self):
        """datetime object representing the last time the issue was updated."""
        return self._updated

    @property
    def user(self):
        """:class:`User <user.User>` who opened the issue."""
        return self._user


class IssueComment(BaseComment):
    """The :class:`IssueComment <IssueComment>` object. This structures and
    handles the comments on issues specifically.
    """
    def __init__(self, comment, session):
        super(IssueComment, self).__init__(comment, session)
        self._user = User(comment.get('user'), self._session)

    def __repr__(self):
        return '<Issue Comment [%s]>' % self._user.login

    @property
    def updated_at(self):
        """datetime object representing the last time the comment was
        updated."""
        return self._updated


class IssueEvent(GitHubCore):
    """The :class:`IssueEvent <IssueEvent>` object. This specifically deals with
    events described in the
    `Issues\>Events <http://developer.github.com/v3/issues/events>`_ section of
    the GitHub API.
    """
    def __init__(self, event, issue):
        super(IssueEvent, self).__init__(event, None)
        # The type of event:
        #   ('closed', 'reopened', 'subscribed', 'merged', 'referenced',
        #    'mentioned', 'assigned')
        self._event = event.get('event')
        self._commit_id = event.get('commit_id')
        self._api = event.get('url')

        # The actual issue in question
        if event.get('issue'):
            self._issue = Issue(event.get('issue'), self._session)
        else:
            self._issue = issue

        # The number of comments
        self._comments = event.get('comments')

        self._closed = None
        if event.get('closed_at'):
            self._closed = self._strptime(event.get('closed_at'))

        self._created = self._strptime(event.get('created_at'))

        self._updated = None
        if event.get('updated_at'):
            self._updated = self._strptime(event.get('updated_at'))

        self._pull_html = None
        self._pull_diff = None
        self._pull_patch = None
        if event.get('pull_request'):
            pull_req = event.get('pull_request')
            self._pull_html = pull_req.get('html_url')
            self._pull_diff = pull_req.get('diff_url')
            self._pull_patch = pull_req.get('patch_url')

    def __repr__(self):
        return '<Issue Event [#%s - %s - %s]>' % (str(self._issue.number),
                self._event, self._actor.login)

    @property
    def event(self):
        """The type of event, e.g., closed"""
        return self._event

    @property
    def commit_id(self):
        """SHA of the commit."""
        return self._commit_id

    @property
    def created_at(self):
        """datetime object representing when the event was created."""
        return self._created

    @property
    def issue(self):
        """:class:`Issue <Issue>` where this comment was made."""
        return self._issue

    @property
    def comments(self):
        """Number of comments"""
        return self._comments


def issue_params(filter, state, labels, sort, direction, since):
    params = []
    if filter in ('assigned', 'created', 'mentioned', 'subscribed'):
        params.append('filter=%s' % filter)

    if state in ('open', 'closed'):
        params.append('state=%s' % state)

    if labels:
        params.append('labels=%s' % labels)

    if sort in ('created', 'updated', 'comments'):
        params.append('sort=%s' % sort)

    if direction in ('asc', 'desc'):
        params.append('direction=%s' % direction)

    if since and match('\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$', since):
        params.append('since=%s' % since)

    return '&'.join(params)
