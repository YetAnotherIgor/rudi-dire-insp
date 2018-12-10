"""
rudi_dire_insp._cli
===================

Command line interface for the project
"""

# Imports from Python distribution
import argparse
import codecs
import json
import logging
import sys
import typing

# Imports from 3rd party

# Imports from this project
import rudi_dire_insp.core as my_core
import rudi_dire_insp.manifests as my_manifests

# Module variables
_LOGGER = logging.getLogger(__name__)
_DEFAULT_LOG_LEVEL = logging.WARNING
_LOGGING_STREAM = sys.stderr


def _parse_cli_args():
    """Parse the command line arguments.

    Returns:
          object: Object produced by the argparse module's parse_args() function.
    """
    # Basic parser setup
    parser = argparse.ArgumentParser(description="Rudimentary directory inspector")

    # Setup mutually exclusive log levels
    log_level_group = parser.add_mutually_exclusive_group()
    log_level_group.add_argument('--verbose', '-v', action='store_true', help="Set log level to INFO")
    log_level_group.add_argument('--debug', '-d', action='store_true', help="Set log level to DEBUG")

    # Add input and output flags/options/args
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        default='-',
        dest='output_path',
        help='Output path for the inspection results')
    parser.add_argument('input_path', type=str, help="The directory to inspect")

    # Run the parser
    parsed_args = parser.parse_args()
    return parsed_args


def _convert_to_json_text(manifest: my_manifests.FileManifest):
    """Translates the manifest object into a JSON object suitable for serialization.

    Args:
          manifest (rudi_dire_insp.manifests.FileManifest): The manifest object to convert

    Returns:
          str: The resultant JSON text
    """
    # Translate the manifest object into 'raw' data that can be processed by the json module
    data = {
        'relative_path': manifest.relative_path,
        'size': manifest.raw_manifest.size,
        'hashes': manifest.raw_manifest.hashes._asdict(),
    }

    # Serialize the raw data into a string.  Use key sorting to allow end-users to diff the
    # output streams.
    json_text = json.dumps(data, sort_keys=True)
    return json_text


def _run_inspection(input_path: str, output_buffer: typing.BinaryIO):
    """Run the inspection on the given input path and write the output to the output writer."""
    writer = codecs.getwriter('utf-8')(output_buffer)
    inspector = my_core.DirectoryInspector()
    counter = 0
    for manifest in inspector.inspect(input_path):
        _LOGGER.debug("Got this manifest from the directory inspector: %s", str(manifest))
        json_text = _convert_to_json_text(manifest)
        writer.write(json_text)
        writer.write("\n")
        counter += 1
    _LOGGER.info("Inspection of directory '%s' produced %d manifest entries", str(input_path), counter)


def main():
    """Main entry point for the CLI"""
    # Parse the command line arguments
    parsed_args = _parse_cli_args()

    # Change log levels depending on the command line options
    if parsed_args.debug:
        log_level = logging.DEBUG
    elif parsed_args.verbose:
        log_level = logging.INFO
    else:
        log_level = None
    if log_level:
        logging.basicConfig(level=log_level, stream=_LOGGING_STREAM)

    # Run the inspection
    if parsed_args.output_path == '-':
        _run_inspection(parsed_args.input_path, sys.stdout.buffer)
    else:
        with open(parsed_args.output_path, 'w+b') as output_file:
            _run_inspection(parsed_args.input_path, output_file)


if __name__ == '__main__':
    logging.basicConfig(level=_DEFAULT_LOG_LEVEL, stream=_LOGGING_STREAM)
    main()
