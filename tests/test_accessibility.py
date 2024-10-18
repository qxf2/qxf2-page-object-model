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
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.mark.ACCESSIBILITY
def test_accessibility(test_obj):
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
            #Check if Axe is run in every page
            run_result = test_obj.accessibility_run_axe()
            # Extract only the violations section
            violations = run_result.get('violations', [])
            current_violations_str = json.dumps(violations, ensure_ascii=False, separators=(',', ':'))

            # Clean the result if needed
            cleaned_current_result = re.sub(r'\\|\n|\r|"timestamp":\s*"[^"]*"', '', current_violations_str)

            # Load the snapshot file and extract the violations section
            snapshot_file_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'snapshots',
                'test_accessibility',
                'test_accessibility',
                'chrome',
                f'snapshot_output_{page}.txt'
            )
            with open(snapshot_file_path, 'r', encoding='utf-8') as snapshot_file:
                snapshot_data = json.load(snapshot_file)

            # Extract the violations section from the snapshot
            snapshot_violations = snapshot_data.get('violations', [])
            snapshot_violations_str = json.dumps(snapshot_violations, ensure_ascii=False, separators=(',', ':'))

            # Compare current violations against the snapshot violations
            snapshot_result = cleaned_current_result == snapshot_violations_str

            test_obj.conditional_write(
                snapshot_result,
                positive=f'Accessibility checks for {page} passed',
                negative=f'Accessibility checks for {page} failed',
                level='debug'
            )

        # Print out the result
        test_obj.write_test_summary()
        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter           

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))

    assert expected_pass == actual_pass, "Test failed: %s"%__file__
