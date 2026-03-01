# Uploads Directory

This directory contains user-uploaded files (Excel files with business processes).

User uploads are automatically ignored by git (see `.gitignore`).

## Usage

When users upload Excel files through the web interface:
1. Files are saved to this directory with unique session-based subdirectories
2. Files are processed and parsed
3. Results are cached for the session

## Cleanup

Old uploads should be cleaned up periodically to save disk space.
