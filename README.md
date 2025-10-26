# FCache

FCache is a simple Python CLI tool to clean Pacman and AUR helper caches on Arch Linux. It supports safe dry runs, deep cleaning, and automatically detects your AUR helper (`yay`, `paru`, `trizen`). Built with `Typer` and `Rich` for a clean CLI experience.

## Features

- Detects AUR helpers automatically.
- Dry-run mode to preview what will be deleted.
- Deep clean mode to remove all cached files.
- Cleans both Pacman and AUR helper caches.

## Installation
```
git clone https://github.com/VxidDev/FCache.git
cd FCache
pip install --editable .
```

## Usage

Run the CLI command:
```
fcache clean --maxvers 3        # Clean Pacman and AUR caches, keeping 3 versions
fcache clean --dryrun           # Preview cleanup without deleting anything
fcache clean --deepclean        # Remove all cached files
```

### Options

- `--maxvers <int>` : Number of versions to keep (default 3)
- `--dryrun` : Show what would be deleted without removing files
- `--deepclean` : Remove all cached files

## Requirements

- Python 3.10+
- `typer`
- `rich`

## Notes

- Requires root privileges for cleaning Pacman cache (`sudo`).
- `deepclean` is destructive; use with caution.
