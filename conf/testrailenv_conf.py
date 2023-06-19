"""
Conf file to hold the TestRail url and credentials
"""
import os
testrail_url = "Add your testrail url"
testrail_user = os.environ.get('TESTRAIL_USERNAME')
testrail_password = os.environ.get('TESTRAIL_PASSWORD')
