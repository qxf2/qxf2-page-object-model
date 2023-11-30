"""
This is an accessibility test to newsletter generator application
Our automated test will do the following:
    #Open Qxf2 newsletter generator application
    #Run accessibility for every page
    #Create snapshot for each page
    #While running the test for first time, use --snapshot-update to create a snapshot folder
"""
import os
import sys
from page_objects.PageFactory import PageFactory
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.mark.ACCESSIBILITY
def test_accessibility(test_obj, snapshot):
    "Inject Axe and create snapshot for every page"

    #Get all pages
    page_names = PageFactory.get_all_page_names()

    for page in page_names:
        test_obj = PageFactory.get_page_object(page,base_url=test_obj.base_url)
        #Inject Axe
        test_obj.accessibility_inject_axe()
        #Run Axe
        result = test_obj.accessibility_run_axe()
        #Create Snapshot
        snapshot.assert_match(f"{result}", f'snapshot_output_{page}.txt')
