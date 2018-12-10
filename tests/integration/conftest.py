"""
Pytest configuration common to all integration tests.
"""

# Imports from Python itself
import logging

# 3rd party imports
import pytest

# this project
from tests.integration.fixtures import cli_json_schema

# Module variables
_LOGGER = logging.getLogger(__name__)


