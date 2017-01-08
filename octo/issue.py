
import json
from datetime import datetime

class Issue(object):
    ''' A generic issue '''

    def __init__(self, subject, **kwargs):
        self.subject = subject
        for name, value in kwargs.items():
            setattr(self, name, value)

        if not hasattr(self, 'date'):
            self.date = {}
            IssueDate(self.date)

    def mii(self):
        pass

    def __dir__(self):
        return dir(super()) + [
            'id',               # the issue id
            'subject',          # the issue short description
            'user',             # the users related to the issue
            'status',           # the issue status
            'tag',              # the issue tags/categories
            'date',             # the issue dates -- see IssueDate
            'field'             # the issue custom fields
        ]

    '''def __getattribute__(self, name):
        value = object.__getattribute__(self, name)
        if name == 'user':
            return IssueUser(value)
        elif name == 'date':
            return IssueDate(value)
        else:
            return value'''

class IssueDate(object):
    ''' Handle issue dates '''

    def __init__(self, data):
        self.__dict__ = data
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

    def __init__(self, data):
        self.__dict__ = data 

    def __dir__(self):
        return dir(super()) + [
            'assigned_to',      # the users responsibles for handle the issue
            'reported_from'     # the users that reported the issue
        ]

class IssueDAO(object):
    ''' Issue Data Access Object '''

    def __init__(self, db):
        self.db = db
        self.issues_db = db.issues

    def load(self, issue_id):
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

        issue_data = issue.__dict__
        updated_issue_data = self.issues_db.find_one_and_replace(
            {'_id': issue_id},
            issue_data,
            new=True,
            upsert=True
        )

        updated_issue = Issue(updated_issue_data)
        return updated_issue
