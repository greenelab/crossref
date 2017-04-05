# Exported MongoDB JSON files

## Files

[![License: CC0 1.0](https://img.shields.io/badge/DOI-10.6084/m9.figshare.4816720-blue.svg)](https://doi.org/10.6084/m9.figshare.4816720)

`crossref-works.json.xz` is not tracked due to large file size (7.4 GB), which exceed the GitHub LFS max size of 2 GB. Instead the file is available [on figshare](https://doi.org/b48h "Metadata for all DOIs in Crossref: JSON MongoDB exports of all works from the Crossref API").
If you use this file, please cite https://doi.org/10.6084/m9.figshare.4816720 (or even better the version-specific DOI).

## Format

`crossref-works.json.xz` is an xz-compressed file of exported works from MongoDB.
It was created using [`mongoexport`](https://docs.mongodb.com/manual/reference/program/mongoexport/) and can be imported into MongoDB using [`mongoimport`](https://docs.mongodb.com/manual/reference/program/mongoimport/).
The file as a whole is not actually valid JSON. However, each line of the file is valid JSON and encodes a single work retrieved from the Crossref API.
Accordingly, you can read this file without `mongoimport` by splitting at newlines and parsing each line as JSON.
