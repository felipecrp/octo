
import json
from datetime import datetime

class Issue(object):
    ''' A generic issue '''

    def __init__(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, dict):
                for name, value in arg.items():
                    setattr(self, name, value)
        for name, value in kwargs.items():
            setattr(self, name, value)

        if not hasattr(self, 'date'):
            setattr(self, 'date', IssueDate())

    def __setattr__(self, name, value):
        if name == '_id':
            object.__setattr__(self, 'id', value)
        elif name == 'user' and isinstance(value, dict):
            object.__setattr__(self, name, IssueUser(**value))
        elif name == 'date' and isinstance(value, dict):
            object.__setattr__(self, name, IssueDate(**value))
        else:
            object.__setattr__(self, name, value)

    def __dir__(self):
        return [
            'id',               # the issue id
            'subject',          # the issue short description
            'user',             # the users related to the issue
            'status',           # the issue status
            'tag',              # the issue tags/categories
            'date',             # the issue dates -- see IssueDate
            'field'             # the issue custom fields
        ]

class IssueDate(object):
    ''' Handle issue dates '''

    def __init__(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, dict):
                for name, value in arg.items():
                    setattr(self, name, value)
        for name, value in kwargs.items():
            setattr(self, name, value)

        if not hasattr(self, 'created'):
            setattr(self, 'created', datetime.now())
        if not hasattr(self, 'last_modified'):
            setattr(self, 'last_modified', datetime.now())

    def __dir__(self):
        return [
            'created',          # when the issue was created
            'last_modified',    # when the issue was last modified
            'closed'            # whem the issue was resolved/closed
        ]

class IssueUser(object):
    ''' Handle issue related users '''

    def __init__(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, dict):
                for name, value in arg.items():
                    setattr(self, name, value)
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __setattr__(self, name, value):
        if isinstance(value, str):
            object.__setattr__(self, name, [value])
        elif isinstance(value, list):
            object.__setattr__(self, name, value)

    def __dir__(self):
        return [
            'assigned_to',      # the users responsibles for handle the issue
            'reported_from'     # the users that reported the issue
        ]

class IssueDAO(object):
    ''' Issue Data Access Object '''

    def __init__(self, db):
        self.db = db
        self.issues_db = db.issues

    def find_one_by_id(self, issue_id):
        ''' Find issue by id '''
        issue_data = self.issues_db.find_one({'_id': issue_id})
        issue = Issue(**issue_data)
        return issue

    def save(self, issue):
        ''' Save the issue '''
        if hasattr(issue, 'id'):
            issue_id = getattr(issue, 'id')
        else:
            issue_id = int(self.db.system_js.getNextSequence('issue'))

        issue_data = self.issues_db.find_one_and_update(
            {
                '_id': issue_id
            },
            {
                '$set': {
                    'subject': getattr(issue, 'subject')
                }
            },
            new=True,
            upsert=True
        )

        updated_issue = Issue(issue_data)
        return updated_issue


