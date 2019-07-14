#!/bin/sh
# Install dependencies on local machine
echo "Installing dev dependencies from NPM"
npm install
echo "Done! Executing command"
exec "$@"
