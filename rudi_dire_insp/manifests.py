"""
rudi_dire_insp.manifests
========================

Manifests for files and directories
"""

# Imports from Python distribution
import copy
import logging
import typing

# Imports from 3rd party

# Imports from this project
import rudi_dire_insp.hashing as my_hashing

# Module variables
_LOGGER = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class RawBytesManifest:
    """A manifest for a set of raw bytes."""

    def __init__(self, hashes: my_hashing.Hashes, size: int):
        """Constructor

        Args:
            hashes (rudi_dire_insp.hashing.Hashes): Hashes of the bytes represented by this manifest.
            size (int): Total number of bytes processed to make the manifest
        """
        # Init private fields
        self._size = int(size)
        self._hashes = hashes

    @property
    def hashes(self) -> my_hashing.Hashes:
        """rudi_dire_insp.hashing.Hashes: A defensive copy of the hashes in this manifest."""
        return copy.copy(self._hashes)

    @property
    def size(self) -> int:
        """int: Total number of bytes processed to create this manifest."""
        return self._size

    def __repr__(self):
        class_name = type(self).__name__
        return '<{} hashes={}, size={}>' .format(class_name, self._hashes, self._size)

    def __str__(self):
        return self.__repr__()


# pylint: disable=too-few-public-methods
class FileManifest:
    """A manifest for an individual file."""

    def __init__(self, relative_path: typing.Tuple[str, ...], raw_manifest: RawBytesManifest):
        """Constructor

        Warning:
              You should not instantiate this class directly.  Instances of it should be retrieved by invoking
              the :py:meth:`rudi_dire_insp.core.DirectoryInspector.inspect`.
        Args:
            relative_path (tuple): The relative path to the file described by this manifest.  Represented as a tuple
                of path elements.  Note: this is relative to the root directory path being inspected.
            raw_manifest (rudi_dire_insp.manifests.RawBytesManifest): The raw manifest describing the file contents.
        """
        self._relative_path = relative_path

        # Verify raw manifest arg
        self._raw_manifest = raw_manifest

    @property
    def relative_path(self) -> typing.Tuple[str, ...]:
        """tuple: Relative path for the file within the inspected directory."""
        return self._relative_path

    @property
    def raw_manifest(self) -> RawBytesManifest:
        """rudi_dire_insp.manifests.RawBytesManifest: Manifest for the file contents."""
        return self._raw_manifest

    def __repr__(self):
        class_name = type(self).__name__
        return '<{} relative_path="{}", raw_manifest={}>' .format(class_name, self._relative_path, self._raw_manifest)

    def __str__(self):
        return self.__repr__()
