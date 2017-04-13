#!/bin/bash
set -e
# Any subsequent(*) commands which fail will cause the shell script to exit immediately

hash curl 2>/dev/null || { echo >&2 "This script requires 'curl', which is not found.  Aborting."; exit 1; }

hash pandoc 2>/dev/null || { echo >&2 "This script requires 'pandoc', which is not found.  Aborting."; exit 1; }

# Make sure we are at the root directory of the repository
cd ${BASH_SOURCE%/*}/..
# Download the markdown readme
echo "Downloading the README.md..."
curl -s -o README.md http://www.craft.ai/content/api/python.md
# Convert to rst
echo "Converting to README.rst..."
pandoc --from=markdown_github --to=rst --output=README.rst README.md

# Commit!
echo "Commiting the two README files"
git add README.md README.rst
git commit -m "Updated README files"

echo "Success!"
