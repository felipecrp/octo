
import json

from pymongo import MongoClient
from flask import Flask
from issue import Issue
from issue import IssueDAO

APP = Flask(__name__)

def main():
    ''' Main Method '''

    client = MongoClient('192.168.99.100', 32769)
    db = client.octo
    issue_dao = IssueDAO(db)
    issue = issue_dao.find_one_by_id(1)
    issue.subject = 'xpto'
    issue_dao.save(issue)
    issue2 = Issue(subject='Teste2')
    issue2 = issue_dao.save(issue2)
    #print('subject: {}'.format(issue.subject))
    #print('created: {}'.format(issue.date.created))
    #print('tags: {}'.format(issue.tag))
    #print('owner: {}'.format(issue.user.assigned_to))
    #print('fields: {}'.format(issue.field))

    for attr in dir(issue):
        if hasattr(issue, attr):
            print('{}: {}'.format(attr, getattr(issue, attr)))

if __name__ == "__main__":
    main()
