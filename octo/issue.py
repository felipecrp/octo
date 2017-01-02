
class Issue(object):
    ''' A generic issue '''

    def __init__(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, dict):
                for key, value in arg.items():
                    self.set(key, value)
        for key, value in kwargs.items():
            self.set(key, value)

    def set(self, key, value):
        if key == '_id':
            setattr(self, 'id', value)
        elif key == 'date':
            setattr(self, key, IssueDate(**value))
        elif key == 'user':
            setattr(self, key, IssueUser(**value))
        else:
            setattr(self, key, value)

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

    def __init__(self, data):
        for attr in data:
            setattr(self, attr, data[attr])

    def __dir__(self):
        return [
            'created',          # when the issue was created
            'last_modified',    # when the issue was last modified
            'closed'            # whem the issue was resolved/closed
        ]

class IssueUser(object):
    ''' Handle issue related people '''

    def __init__(self, data):
        for attr in data:
            setattr(self, attr, data[attr])

    def __dir__(self):
        return [
            'assigned_to',      # the users responsibles for handle the issue
            'reported_from'     # the users that reported the issue
        ]

if __name__ == "__main__":
    b = Issue(subject='xpto2')
    a = Issue({ 'subject': 'xpto'})
