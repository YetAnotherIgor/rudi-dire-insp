"""
rudi_dire_insp.hashing
======================

Utility plumbing for calculating cryptographic hashes.
"""

# Imports from Python distribution
import collections
import enum
import hashlib
import logging
import typing

# Imports from 3rd party

# Imports from this project
import rudi_dire_insp.exceptions as my_exceptions

# Module variables
_LOGGER = logging.getLogger(__name__)

Hashes = collections.namedtuple("Hashes", ['md5', 'sha1', 'sha256', 'sha384', 'sha512'])
"""A set of hex string values for hashes calculated from the same binary dataset.

The string containing the hex value for each is available via an object attribute of
the same name.
"""


# pylint: disable=too-few-public-methods,unnecessary-lambda
class _HashAlgorithm(enum.Enum):
    """Hashing algorithms used to fingerprint inspected files."""

    MD5 = (1, lambda: hashlib.md5())
    """MD5 algorithm"""

    SHA1 = (2, lambda: hashlib.sha1())
    """SHA1 algorithm"""

    SHA256 = (3, lambda: hashlib.sha256())
    """SHA256 algorithm"""

    SHA384 = (4, lambda: hashlib.sha384())
    """SHA384 algorithm"""

    SHA512 = (5, lambda: hashlib.sha512())
    """SHA512 algorithm"""

    def __init__(self, ordinal: int, digest_constructor: typing.Callable):
        """Constructor

        Args:
            ordinal (int): The ordering number used for the enumeration instance.
            digest_constructor (Callable): The function instance to invoke when calculating the hash according
                to the algorithm represented by this enumeration instance.
        """

        self._ordinal = ordinal
        self._digest_constructor = digest_constructor

    def _new_digest(self):
        """Create a new instance of a digest.

        Note:
            Using a custom approach instead of ``hashlib.new('sha256')`` style because the Python
            API docs say that way is "slower".

        Returns:
            hashlib.Digest
        """
        digest = self._digest_constructor()
        return digest

    @staticmethod
    def calculate_hashes(stream: typing.BinaryIO) -> typing.Tuple[Hashes, int]:
        """Calculate the hashes for the content at tha path

        Args:
            stream (typing.BinaryIO): The source for the binary data to calculate the hashes from.

        Returns:
            tuple: A tuple consisting of (:py:class:`rudi_dire_insp.hashing.Hashes`, :py:class:`int`)

        Raises:
            rudi_dire_insp.exceptions.HashError
        """
        _LOGGER.debug("Begin calculating hashes using a byte stream reader")
        # Setup all the digests
        digests = {}
        for digest_enum in _HashAlgorithm:
            # pylint: disable=protected-access
            digests[digest_enum] = digest_enum._new_digest()

        # Read the stream and update the digests on the way
        num_read = 0
        try:
            while True:
                buffer = stream.read()
                if buffer:
                    num_read += len(buffer)
                    for digest in digests.values():
                        digest.update(buffer)
                else:
                    break
        except Exception as error:
            raise my_exceptions.HashError("Error calculating hashes") from error

        # Return the hex values for the accumulated digests
        hashes_params = {}
        for digest_enum, digest in digests.items():
            hashes_params[digest_enum.name.lower()] = digest.hexdigest()
        hashes = Hashes(**hashes_params)

        if _LOGGER.isEnabledFor(logging.DEBUG):
            _LOGGER.debug("Calculated these hashes using a byte stream reader: %s", str(hashes))
            _LOGGER.debug("Total number of bytes read was: %d", num_read)

        _LOGGER.debug("Finished calculating hashes using a byte stream reader")
        return hashes, num_read
