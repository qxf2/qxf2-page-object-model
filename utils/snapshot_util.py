"""
Snapshot Integration
* This is a class which holds limited methods we need for the moment
"""

import os
from pathlib import Path
import operator
from typing import Union
from pytest_snapshot._utils import shorten_path, _pytest_expected_on_right

snapshot_dir = (Path(__file__).resolve().parent.parent / 'tests' / 'snapshots' / 'test_accessibility' / 'test_accessibility' / 'chrome').absolute()

def _assert_equal(value, snapshot) -> None:
    if _pytest_expected_on_right():
        assert value == snapshot
    else:
        assert snapshot == value

def _file_encode(string: str) -> bytes:
    """
    Returns the bytes that would be in a file created using ``path.write_text(string)``.
    See universal newlines documentation.
    """
    if '\r' in string:
        raise ValueError('''\
Snapshot testing strings containing "\\r" is not supported.
To snapshot test non-standard newlines you should convert the tested value to bytes.
Warning: git may decide to modify the newlines in the snapshot file.
To avoid this read \
https://docs.github.com/en/get-started/getting-started-with-git/configuring-git-to-handle-line-endings''')

    return string.replace('\n', os.linesep).encode()

def _file_decode(data: bytes) -> str:
    """
    Returns the string that would be read from a file using ``path.read_text(string)``.
    See universal newlines documentation.
    """
    return data.decode().replace('\r\n', '\n').replace('\r', '\n')

class Snapshotutil():
    "Snapshot object to compare snapshots"
    def __init__(self, snapshot_update: bool = False, allow_snapshot_deletion: bool = False):
        self._snapshot_update = snapshot_update
        self._allow_snapshot_deletion = allow_snapshot_deletion
        self.snapshot_dir = snapshot_dir
        self._created_snapshots = []
        self._updated_snapshots = []
        self._snapshots_to_delete = []

    @property
    def snapshot_dir(self):
        return self._snapshot_dir

    @snapshot_dir.setter
    def snapshot_dir(self, value):
        self._snapshot_dir = Path(value).absolute()

    def _snapshot_path(self, snapshot_name: Union[str, Path]) -> Path:
        """
        Returns the absolute path to the given snapshot.
        """
        if isinstance(snapshot_name, Path):
            snapshot_path = snapshot_name.absolute()
            return snapshot_path
        else:
            snapshot_path = self.snapshot_dir.joinpath(snapshot_name)

        # TODO: snapshot_path = snapshot_path.resolve(strict=False). Requires Python >3.6 for strict=False.
        if self.snapshot_dir not in snapshot_path.parents:
            raise ValueError('Snapshot path {} is not in {}'.format(
                shorten_path(snapshot_path), shorten_path(self.snapshot_dir)))

        return snapshot_path

    def _get_compare_encode_decode(self, value: Union[str, bytes]):
        """
        Returns a 3-tuple of a compare function, an encoding function, and a decoding function.

        * The compare function should compare the object to the value of its snapshot,
          raising an AssertionError with a useful error message if they are different.
        * The encoding function should encode the value into bytes for saving to a snapshot file.
        * The decoding function should decode bytes from a snapshot file into a object.
        """
        if isinstance(value, str):
            return _assert_equal, _file_encode, _file_decode
        elif isinstance(value, bytes):
            return _assert_equal, lambda x: x, lambda x: x
        else:
            raise TypeError('value must be str or bytes')

    def assert_match(self, value: Union[str, bytes], snapshot_name: Union[str, Path]):
        """
        Asserts that ``value`` equals the current value of the snapshot with the given ``snapshot_name``.

        If pytest was run with the --snapshot-update flag, the snapshot will instead be updated to ``value``.
        The test will fail if there were any changes to the snapshot.
        """
        __tracebackhide__ = operator.methodcaller("errisinstance", AssertionError)
        compare, encode, decode = self._get_compare_encode_decode(value)
        snapshot_path = self._snapshot_path(snapshot_name)
        if snapshot_path.is_file():
            encoded_expected_value = snapshot_path.read_bytes()
        elif snapshot_path.exists():
            raise AssertionError('snapshot exists but is not a file: {}'.format(shorten_path(snapshot_path)))
        else:
            encoded_expected_value = None

        if self._snapshot_update:
            encoded_value = encode(value)
            if encoded_expected_value is None or encoded_value != encoded_expected_value:
                decoded_encoded_value = decode(encoded_value)
                if decoded_encoded_value != value:
                    raise ValueError("value is not supported by pytest-snapshot's serializer.")

                snapshot_path.parent.mkdir(parents=True, exist_ok=True)
                snapshot_path.write_bytes(encoded_value)
                if encoded_expected_value is None:
                    self._created_snapshots.append(snapshot_path)
                else:
                    self._updated_snapshots.append(snapshot_path)
        else:
            if encoded_expected_value is not None:
                expected_value = decode(encoded_expected_value)
                try:
                    compare(value, expected_value)
                except AssertionError as e:
                    snapshot_diff_msg = str(e)
                else:
                    snapshot_diff_msg = None

                if snapshot_diff_msg is not None:
                    snapshot_diff_msg = 'value does not match the expected value in snapshot {}\n' \
                                        '  (run pytest with --snapshot-update to update snapshots)\n{}'.format(
                                            shorten_path(snapshot_path), snapshot_diff_msg)
                    raise AssertionError(snapshot_diff_msg)
            else:
                raise AssertionError(
                    "snapshot {} doesn't exist. (run pytest with --snapshot-update to create it)".format(
                        shorten_path(snapshot_path)))
            