"""This package contains unit tests for the project."""

from six import add_move, MovedModule
add_move(MovedModule('mock', 'mock', 'unittest.mock'))
