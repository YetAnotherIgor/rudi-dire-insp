"""
Unit tests for the rudi_dire_insp.hashing module.
"""

# Core python imports
import hashlib
import io
import logging

# 3rd party imports
import pytest

# Imports of code-under-test
import rudi_dire_insp.exceptions as my_exceptions
import rudi_dire_insp.hashing as my_hashing

# Module variables
_LOGGER = logging.getLogger(__name__)
pytestmark = pytest.mark.unit


def test_digest_error():
    """Smoke test error handling during digest calculations"""
    _LOGGER.debug("Begin test")
    test_stream = "I'm not a binary stream!"

    with pytest.raises(my_exceptions.HashError):
        my_hashing._HashAlgorithm.calculate_hashes(test_stream)

    _LOGGER.debug("Finished test")


def _calculate_hash_hex(algorithm_name: str, data: bytes) -> str:
    """Calculate the hex value of the digest of a the binary
     data using the named algorithm"""

    digest = hashlib.new(algorithm_name)
    digest.update(data)
    return digest.hexdigest()


def test_which_algorithm():
    """Verify that the right underlying digest algorithm provider is wired up to the write enum from this project"""
    _LOGGER.debug("Begin test")

    # Prepare test data and expected hashing results
    test_data = b'hello world'
    expected_hashes_kwargs = {
        algorithm_name: _calculate_hash_hex(algorithm_name, test_data)
        for algorithm_name in ['md5', 'sha1', 'sha256', 'sha384', 'sha512']
    }
    expected_hashes = my_hashing.Hashes(**expected_hashes_kwargs)
    expected_size = len(test_data)

    # Now calculate the hashes using the code-under-test
    test_stream = io.BytesIO(test_data)
    (hashes, size) = my_hashing._HashAlgorithm.calculate_hashes(test_stream)

    # Verify expected and found match
    assert expected_hashes == hashes
    assert expected_size == size

    _LOGGER.debug("Finished test")
