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
import logging
import pytest
from page_objects.PageFactory import PageFactory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.DEBUG)

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
            # Define snapshot file path (use .json for snapshots)
            snapshot_file = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'snapshots',
                'test_accessibility',
                'test_accessibility',
                'chrome',
                f'snapshot_output_{page}.json'
            )
            # Load saved snapshot if it exists
            saved_snapshot = load_snapshot(snapshot_file)

            # If no snapshot exists, save the current violations[] as the new snapshot
            if saved_snapshot is None:
                logging.debug(f"No snapshot found for {page}, creating a new snapshot.")
                save_snapshot(snapshot_file, violations)
                snapshot_result = True
            else:
                # Compare the saved snapshot with the current violations[]
                cleaned_result = json.dumps(violations, ensure_ascii=False, separators=(',', ':'))
                cleaned_snapshot = json.dumps(saved_snapshot, ensure_ascii=False, separators=(',', ':'))

                # Snapshot comparison
                snapshot_result = (cleaned_result == cleaned_snapshot)

            test_obj.conditional_write(snapshot_result,
                                       positive=f'Accessibility checks for {page} passed',
                                       negative=f'Accessibility checks for {page} failed',
                                       level='debug')

        # Print out the result
        test_obj.write_test_summary()
        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter           

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))

    assert expected_pass == actual_pass, "Test failed: %s"%__file__



def load_snapshot(snapshot_file):
    """Load the saved snapshot from a JSON file."""
    if os.path.exists(snapshot_file):
        with open(snapshot_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    return None

def save_snapshot(snapshot_file, data):
    """Save the given data as a snapshot in a JSON file."""
    with open(snapshot_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)