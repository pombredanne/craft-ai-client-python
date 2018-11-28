#!/bin/bash
set -e
# Any subsequent(*) commands which fail will cause the shell script to exit immediately

hash curl 2>/dev/null || { echo >&2 "This script requires 'curl', which is not found.  Aborting."; exit 1; }

# Make sure we are at the root directory of the repository
cd ${BASH_SOURCE%/*}/..
# Download the markdown readme
echo "Downloading the README.md..."
curl -s -o README.md https://www.craft.ai/content/api/python.md

# Commit!
echo "Commiting the README file"
git add README.md
git commit -m "Updated README file"

echo "Success!"
