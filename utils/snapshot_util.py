"""
Snapshot Integration
* This is a class which extends the methods of Snapshot parent class
"""
import os
import json
from pytest_snapshot.plugin import Snapshot
import conf.snapshot_dir_conf

snapshot_dir = conf.snapshot_dir_conf.snapshot_dir

class Snapshotutil(Snapshot):
    "Snapshot object to use snapshot for comparisions"
    def __init__(self, snapshot_update=False,
                 allow_snapshot_deletion=False,
                 snapshot_dir=snapshot_dir):
        super().__init__(snapshot_update, allow_snapshot_deletion, snapshot_dir)

    def load_snapshot(self, snapshot_file_path):
        "Load the saved snapshot from a JSON file."
        if os.path.exists(snapshot_file_path):
            with open(snapshot_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        return None

    def save_snapshot(self, snapshot_file_path, current_violations):
        "Save the given data as a snapshot in a JSON file."
        os.makedirs(os.path.dirname(snapshot_file_path), exist_ok=True)
        with open(snapshot_file_path, 'w', encoding='utf-8') as file:
            json.dump(current_violations, file, ensure_ascii=False, indent=4)

    def find_new_violations(self, current_violations, existing_snapshot):
        "Return a list of new violations that are not in the saved snapshot."
        new_violations = []
        for violation in current_violations:
            if violation not in existing_snapshot:
                new_violations.append(violation)
        return new_violations

    def sanitize_html(self, html):
        "Replace charmap characters so read html."
        return ''.join(c if ord(c) < 128 else '?' for c in html)

    def get_new_violations(self, current_violations_json, existing_snapshot_json, page):
        "Compares the snapshots and prints the new violations"
        # Load the results from JSON strings
        new_violations = json.loads(current_violations_json)
        saved_snapshot = json.loads(existing_snapshot_json)

        # Create a set of existing HTML elements from the saved snapshot
        existing_html_elements = set()
        for saved_item in saved_snapshot:
            for saved_node in saved_item['nodes']:
                if saved_node['any']:
                    for violation in saved_node['any']:
                        for related in violation['relatedNodes']:
                            existing_html_elements.add(related['html'])

        # Set to track printed elements
        new_violation_details = []

        # Compare new violations and add new violation HTML elements not in the snapshot
        for new_item in new_violations:
            for new_node in new_item['nodes']:
                if new_node['any']:
                    for violation in new_node['any']:
                        for related in violation['relatedNodes']:
                            # Add only if the HTML is not in the existing snapshot
                            if related['html'] not in existing_html_elements:
                                sanitized_html = self.sanitize_html(related['html'])
                                new_violation_details.append({
                                    "page": page,
                                    "id": new_item.get('id', 'unknown'),
                                    "impact": new_item.get('impact', 'unknown'),
                                    "description": new_item.get('description', 'unknown'),
                                    "html": sanitized_html
                                })
        return new_violation_details
