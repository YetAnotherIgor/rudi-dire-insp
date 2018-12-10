######
README
######

This is a toy implementation of a rudimentary directory inspector.

The "inspection" consists of traversing a designated directory's contents,
and generating a stream of file manifests based on the files inside
that directory and its sub-directories.

The file manifests include the following:

* Hex values for a plethora of cryptographic hashes of the file contents
* The size of the file (in bytes)
* The "path" to the file represented as an array of file path elements 
  relative to the starting directory for the inspection.

Please see the included Sphinx docs for (under ``docs``) for more information.
