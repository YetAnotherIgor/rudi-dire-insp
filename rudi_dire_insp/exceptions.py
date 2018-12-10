"""
rudi_dire_insp.exceptions
=========================

Exceptions specific to this project.
"""


class RudiDireInspException(Exception):
    """Parent exception class for all exceptions specific to this project."""


class DirInspectionError(RudiDireInspException):
    """An exception raised during inspection of a directory."""


class FileInspectionError(RudiDireInspException):
    """An exception raised during inspection of a file."""


class HashError(RudiDireInspException):
    """An exception raised during the calculation or verification of a cryptographic hash."""
