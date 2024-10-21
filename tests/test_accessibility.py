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
            #Extract only the violations section
            violations = run_result.get('violations', [])
            #Snapshot file path to load
            snapshot_file = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'snapshots',
                'test_accessibility',
                'test_accessibility',
                'chrome',
                f'snapshot_output_{page}.json'
            )
            saved_snapshot = None
            if os.path.exists(snapshot_file):
                with open(snapshot_file, 'r', encoding='utf-8') as file:
                    saved_snapshot = json.load(file)

            #If snapshot not exists, save the current violations[] as the new snapshot
            if saved_snapshot is None:
                with open(snapshot_file, 'w', encoding='utf-8') as file:
                    json.dump(violations, file, ensure_ascii=False, indent=4)
                snapshot_result = True
            else:
                #Compare the saved snapshot with the current violations[]
                cleaned_result = json.dumps(violations, ensure_ascii=False, separators=(',', ':'))
                cleaned_snapshot = json.dumps(saved_snapshot, 
                                              ensure_ascii=False, 
                                              separators=(',', ':'))
                #Check if there are new violations
                new_violations = [v for v in violations if v not in saved_snapshot]
                if new_violations:
                    print(f"New violations found on {page}:")
                    for violation in new_violations:
                        print(
                            f"- ID: {violation['id']}, "
                            f"Impact: {violation['impact']}, "
                            f"Description: {violation['description']}"
                        )

                #Snapshot comparison
                snapshot_result = cleaned_result == cleaned_snapshot

            test_obj.log_result(snapshot_result,
                                 positive=f'Accessibility checks for {page} passed',
                                 negative=f'Accessibility checks for {page} failed',
                                 level='debug')

        #Print out the result
        test_obj.write_test_summary()
        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter

    except Exception as e:
        print(f"Exception when trying to run test: {__file__}")
        print(f"Python says: {str(e)}")

    assert expected_pass == actual_pass, f"Test failed: {__file__}"
