
class Issue(object):
    ''' A generic issue '''
    def __init__(self, data):
        for attr in data:
            if attr == '_id':
                setattr(self, 'id', data[attr])
            else:
                setattr(self, attr, data[attr])

    def __dir__(self):
        return ['id', 'subject', 'logs', 'date_fields', 'custom_fields']

