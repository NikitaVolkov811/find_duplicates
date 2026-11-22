# find-duplicates

A command-line tool that finds duplicate files by content and moves the extra copies to the trash.

## Why

Duplicates pile up in download folders and photo archives: the same file gets
saved twice and ends up as `photo.jpg` and `photo (1).jpg`. Comparing file names
does not find them, because the names are different — and most operating systems
will not even allow two identical names in one folder.

This tool compares file **content** instead of names.

## How it works

Each file is read in 1 MB chunks and hashed with MD5. Files with the same hash
are grouped together. Inside a group the file with the shortest name is kept
(ties are broken alphabetically), and the rest are reported as copies.

## Usage

```
python find_duplicates.py "path/to/folder"            # report only
python find_duplicates.py "path/to/folder" --delete   # report, then ask to delete
```

Deleting is off by default. With `--delete` the tool prints the report first and
asks for confirmation. Confirmed files are moved to the system trash, not erased
permanently, so a mistake can be undone.

Example output:

```
Keep: 4.jpg
  Delete: 4 - copy.jpg (0.68 MB)
Keep: Job_Tracker_50.xlsx
  Delete: Job_Tracker_50 (1).xlsx (0.02 MB)

Duplicate files: 2
Wasted space: 0.7 MB
Move these files to trash? (y/n):
```

## Requirements

Python 3.x and one dependency:

```
pip install -r requirements.txt
```

## Limitations

- Only byte-for-byte identical files are detected. Visually similar images are
  not: a RAW file and the JPEG exported from it have different content, and so
  do two versions of the same photo saved at different quality.
- Only the given folder is scanned; subfolders are ignored.
- The rule for which file to keep is fixed (shortest name) and cannot be changed
  from the command line.

## Possible next steps

- Recursive scanning of subfolders
- Perceptual hashing to find visually similar images
- A `--keep` option to choose the rule (oldest file, shortest name, custom)
- Byte-for-byte comparison as a final check before deleting, to rule out hash collisions
