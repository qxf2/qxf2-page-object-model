"""
This is a test file to run accessibility test on
    1. Selenium tutorial main page
    2. Selenium tutorial redirect page
    3. Selenium tutorial contact page
    #While running the test for first time, use --snapshot-update to create a snapshot folder
"""
import os
import sys
import time
import json
import re
import pytest
from page_objects.PageFactory import PageFactory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.mark.ACCESSIBILITY
def test_accessibility(test_obj):
    "Inject Axe and create snapshot for every page"
    try:

        #Initalize flags for tests summary
        expected_pass = 0
        actual_pass = -1

        #Set start_time with current time
        start_time = int(time.time())

        #Get all pages
        page_names = PageFactory.get_all_page_names()

        for page in page_names:
            test_obj = PageFactory.get_page_object(page,base_url=test_obj.base_url)
            #Inject Axe in every page
            test_obj.accessibility_inject_axe()
            #Check if Axe is run in every page
            run_result = test_obj.accessibility_run_axe()
            if run_result is not None:
                test_obj.log_result(True,
                                positive="Ran axe in %s"%page,
                                negative="Unable to run axe in %s"%page)
            test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
            #Serialize dict to JSON-formatted string
            result_str = json.dumps(run_result, ensure_ascii=False, separators=(',', ':'))
            #Formatting result by removing \n,\\,timestamp
            #Every test run have a different timestamp.
            cleaned_result = re.sub(r'\\|\n|\r|"timestamp":\s*"[^"]*"', '', result_str)
            #Compare Snapshot for each page
            test_obj.snapshot_assert_match(f"{cleaned_result}", f'snapshot_output_{page}.txt')

        #Print out the result
        test_obj.write_test_summary()
        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))

    assert expected_pass == actual_pass, "Test failed: %s"%__file__
