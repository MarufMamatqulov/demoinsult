#!/usr/bin/env bash
# build.sh for Render.com deployment

# Exit on error
set -o errexit

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt

# Make sure scripts directory exists
mkdir -p "${HOME}/scripts"

# Copy scripts to home dir (for accessibility and permissions)
cp start_backend.sh "${HOME}/scripts/"
chmod +x "${HOME}/scripts/start_backend.sh"

echo "Build completed successfully!"
