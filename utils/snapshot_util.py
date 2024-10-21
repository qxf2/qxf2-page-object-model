"""
Snapshot Integration
* This is a class which extends the methods of Snapshot parent class
"""
import os
import json
import conf.snapshot_dir_conf
from pytest_snapshot.plugin import Snapshot

snapshot_dir = conf.snapshot_dir_conf.snapshot_dir

class Snapshotutil(Snapshot):
    "Snapshot object to use snapshot for comparisions"
    def __init__(self, snapshot_update=False,
                 allow_snapshot_deletion=False,
                 snapshot_dir=snapshot_dir):
        super().__init__(snapshot_update, allow_snapshot_deletion, snapshot_dir)

    def load_snapshot(self, snapshot_file):
        """Load the saved snapshot from a JSON file."""
        if os.path.exists(snapshot_file):
            with open(snapshot_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        return None

    def save_snapshot(self, snapshot_file, violations):
        """Save the given data as a snapshot in a JSON file."""
        with open(snapshot_file, 'w', encoding='utf-8') as file:
            json.dump(violations, file, ensure_ascii=False, indent=4)
