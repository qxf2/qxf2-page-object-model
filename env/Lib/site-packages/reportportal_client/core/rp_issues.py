"""This module includes classes representing RP issues.

Issues are reported within the test item result PUT call. One issue can be
associated with multiple external issues. By external issues is meant issues
at the existing bug tracker systems. The following keys need to be sent in
order to add an issue to the test result:

{
  ...,
  "issue": {
    "autoAnalyzed": true,
    "comment": "string",
    "externalSystemIssues": [
      {
        "btsProject": "string",
        "btsUrl": "string",
        "submitDate": 0,
        "ticketId": "string",
        "url": "string"
      }
    ],
    "ignoreAnalyzer": true,
    "issueType": "string"
  }
  ...
}

Copyright (c) 2018 http://reportportal.io .

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


class Issue(object):
    """This class represents an issue that can be attached to test result."""

    def __init__(self,
                 issue_type,
                 comment=None,
                 auto_analyzed=False,
                 ignore_analyzer=True):
        """Initialize instance attributes.

        :param issue_type:      Issue type locator. Allowable values: "pb***",
                                "ab***", "si***", "ti***", "nd001". Where ***
                                is locator id.
        :param comment:         Issue comments
        :param auto_analyzed:   Indicator that the issue has been marked with
                                the RP auto analyzer
        :param ignore_analyzer: Flag that forces RP analyzer to ignore this
                                issue
        """
        self._external_issues = []
        self.auto_analyzed = auto_analyzed
        self.comment = comment
        self.ignore_analyzer = ignore_analyzer
        self.issue_type = issue_type

    def external_issue_add(self, issue):
        """Add external system issue to the issue."""
        self._external_issues.append(issue.payload)

    @property
    def payload(self):
        """Form the correct dictionary for the issue."""
        return {
            'autoAnalyzed': self.auto_analyzed,
            'comment': self.comment,
            'externalSystemIssues': self._external_issues,
            'ignoreAnalyzer': self.ignore_analyzer,
            'issueType': self.issue_type
        }


class ExternalIssue(object):
    """This class represents external(BTS) system issue."""

    def __init__(self,
                 bts_url=None,
                 bts_project=None,
                 submit_date=None,
                 ticket_id=None,
                 url=None):
        """Initialize instance attributes.

        :param bts_url:     Bug tracker system URL
        :param bts_project: Bug tracker system project
        :param submit_date: Bug submission date
        :param ticket_id:   Unique ID of the ticket at the BTS
        :param url:         URL to the ticket(bug)
        """
        self.bts_url = bts_url
        self.bts_project = bts_project
        self.submit_date = submit_date
        self.ticket_id = ticket_id
        self.url = url

    @property
    def payload(self):
        """Form the correct dictionary for the BTS issue."""
        return {
            'brsUrl': self.bts_url,
            'btsProject': self.bts_project,
            'submitDate': self.submit_date,
            'ticketId': self.ticket_id,
            'url': self.url
        }
