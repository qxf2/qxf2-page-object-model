"""
This is a test file to run accessibility test on
    1. Selenium tutorial main page
    2. Selenium tutorial redirect page
    3. Selenium tutorial contact page
    #While running the test for first time, use --snapshot-update to create a snapshot folder
"""
import os
import sys
import json
import re
import pytest
from page_objects.PageFactory import PageFactory
from utils.Option_Parser import Option_Parser
import conf.testrail_caseid_conf as testrail_file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.mark.ACCESSIBILITY
def test_accessibility(test_obj, snapshot):
    "Inject Axe and create snapshot for every page"
    try:

        #Initalize flags for tests summary
        expected_pass = 0
        actual_pass = -1
        #Get all pages
        page_names = PageFactory.get_all_page_names()

        for page in page_names:
            test_obj = PageFactory.get_page_object(page,base_url=test_obj.base_url)
            #Inject Axe in every page
            test_obj.accessibility_inject_axe()
            #Run Axe in every page
            result = test_obj.accessibility_run_axe()
            #Serialize dict to JSON-formatted string
            result_str = json.dumps(result, ensure_ascii=False, separators=(',', ':'))
            #Formatting result by removing \n,\\,timestamp
            #Every test run have a different timestamp.
            cleaned_result = re.sub(r'\\|\n|\r|"timestamp":\s*"[^"]*"', '', result_str)
            #Create Snapshot
            snapshot.assert_match(f"{cleaned_result}", f'snapshot_output_{page}.txt')

        #5. Print out the result
        test_obj.write_test_summary()
        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))

    assert expected_pass == actual_pass, "Test failed: %s"%__file__
