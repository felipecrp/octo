
import json

from pymongo import MongoClient
from flask import Flask
from issue import Issue

APP = Flask(__name__)

def main():
    ''' Main Method '''
    #APP.run()
    get_issue(1)

def get_issues():
    ''' Get all isssues '''
    issues = db.issues.find({})

    for issue in issues:
        print('ticket id: {}'.format(issue['_id']))
        if 'name' in issue:
            print('\tname: {}'.format(issue['name']))
        if 'ref' in issue:
            print('\tref: {}'.format(issue['ref']))

@APP.route("/issue/<issue_id>")
def get_issue(issue_id):
    ''' Return an issue '''
    client = MongoClient('192.168.99.100', 32769)
    db = client.octo
    issue_data = db.issues.find_one({'_id': issue_id})
    issue = Issue(issue_data)

    print(type(issue))
    print(issue)
    # return json.dumps(issue_data)

    # issue = Issue()
    # issue.id = 1
    # issue.subject = 'abc'
    #return json.dumps(dict((name, getattr(issue, name)) for name in dir(issue) if not name.startswith('__') and hasattr(issue,name)))

if __name__ == "__main__":
    main()
