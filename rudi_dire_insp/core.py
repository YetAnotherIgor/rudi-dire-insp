"""
rudi_dire_insp.core
===================

Core stuff
"""

# Imports from Python distribution
import logging
import os
import typing

# Imports from 3rd party

# Imports from this project
import rudi_dire_insp.exceptions as my_exceptions
import rudi_dire_insp.hashing as my_hashing
import rudi_dire_insp.manifests as my_manifests

# Module variables
_LOGGER = logging.getLogger(__name__)


def _raise_if_bad_root_directory(path: str):
    """Raise an exception if the candidate root directory is not a directory, or does not exist
    Args:
          path (str): Path to the candidate root directory
    Raises:
        rudi_dire_insp.exceptions.DirInspectionError
    """
    if not os.path.exists(path):
        raise my_exceptions.DirInspectionError("Root directory path does not exist: '{}'".format(path))
    if not os.path.isdir(path):
        raise my_exceptions.DirInspectionError("Root directory path exists, but is not a directory: {}".format(path))


# pylint: disable=no-self-use,too-few-public-methods
class _FileInspector:
    """Inspector for a file."""

    def __init__(self, root_dir_path: str):
        """Constructor

        Args:
            root_dir_path (str): The path to the root of the directory structure that contains the file
                being inspected.  This is the "root" in terms of the overall set of files and directories
                being inspected, not necessarily the absolute path to the root of the file system etc.

        Raises:
            rudi_dire_insp.exceptions.DirInspectionError
        """
        _raise_if_bad_root_directory(root_dir_path)
        self._root_dir_path = root_dir_path
        self._real_root_dir_path = os.path.realpath(self._root_dir_path)

    def _raise_if_not_sub_path(self, path: str):
        """Raises an exception of the given path is not a sub path of the root directory path being inspected.

        Args:
            path (str): The path being checked.

        Raises:
            rudi_dire_insp.exceptions.FileInspectionError
            rudi_dire_insp.exceptions.DirInspectionError
        """
        real_path = os.path.realpath(path)
        if not real_path.startswith(self._real_root_dir_path):
            raise my_exceptions.FileInspectionError(
                "File path is not a child of the root directory path '{}' : '{}'".format(
                    self._root_dir_path, path))

    def _inspect_stream(self, stream: typing.BinaryIO) -> my_manifests.RawBytesManifest:
        """Inspects the given byte stream and returns an incomplete manifest entry for it.

        Args:
            stream (typing.BinaryIO): The binary input representing the file content being inspected.

        Returns:
            rudi_dire_insp.manifests.FileManifest
        """
        # pylint: disable=protected-access
        (hashes, size) = my_hashing._HashAlgorithm.calculate_hashes(stream)
        manifest = my_manifests.RawBytesManifest(hashes, size)

        if _LOGGER.isEnabledFor(logging.DEBUG):
            _LOGGER.debug("Created raw bytes manifest for byte stream: %s", str(manifest))
        return manifest

    def inspect(self, path: str) -> my_manifests.FileManifest:
        """Inspect the file at the given path and returns a manifest entry for it.

        Args:
            path (str): The path on the file system to inspect.  Must be a child of the root directory path
                used as a parameter to the constructor of this class.

        Returns:
            rudi_dire_insp.manifests.FileManifest
        """
        # Verify the path points to a file
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            raise my_exceptions.FileInspectionError("File at path does not exist: {}".format(abs_path))
        if not os.path.isfile(abs_path):
            raise my_exceptions.FileInspectionError("Path does not point to a file: {}".format(abs_path))
        self._raise_if_not_sub_path(path)

        # Build the manifest
        with open(abs_path, 'rb') as input_file:
            raw_manifest = self._inspect_stream(input_file)
            relative_path = os.path.relpath(abs_path, self._root_dir_path)
            rel_path_as_tuple = os.path.split(relative_path)
            file_manifest = my_manifests.FileManifest(rel_path_as_tuple, raw_manifest)

        if _LOGGER.isEnabledFor(logging.DEBUG):
            _LOGGER.debug("Created file manifest for file %s : %s", abs_path, str(file_manifest))

        return file_manifest


# pylint: disable=no-self-use,too-few-public-methods
class DirectoryInspector:
    """Inspector for the top-most directory being inspected."""

    def __init__(self):
        """Constructor"""

    def inspect(self, path: str) -> typing.Iterable[my_manifests.FileManifest]:
        """Inspect the directory and its contents, starting at the given path.

        Acts as a Python generator (yielding manifests as return values)

        Args:
            path (str): The path to the directory on the file system to inspect.

        Yields:
            rudi_dire_insp.manifests.FileManifest: FileManifest for a file within the path inspected.

        Raises:
            rudi_dire_insp.exceptions.DirInspectionError
            rudi_dire_insp.exceptions.FileInspectionError
            rudi_dire_insp.exceptions.HashError
        """
        # Verify function arg
        _raise_if_bad_root_directory(path)

        # Create a file inspector
        file_inspector = _FileInspector(path)

        # Walk the directory and yield manifests
        abs_path = os.path.abspath(path)
        for dir_path, _, file_names in os.walk(abs_path):
            for file_name in file_names:
                file_path = os.path.join(dir_path, file_name)
                file_manifest = file_inspector.inspect(file_path)
                yield file_manifest
