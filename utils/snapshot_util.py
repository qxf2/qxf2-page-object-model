"""
Snapshot Integration
* This is a class which extends the methods of Snapshot parent class
"""

import conf.snapshot_dir_conf
from pytest_snapshot.plugin import Snapshot

snapshot_dir = conf.snapshot_dir_conf.snapshot_dir

class Snapshotutil(Snapshot):
    "Snapshot object to use snapshot for comparisions"
    def __init__(self, snapshot_update=False,
                 allow_snapshot_deletion=False,
                 snapshot_dir=snapshot_dir):
        super().__init__(snapshot_update, allow_snapshot_deletion, snapshot_dir)
