import argparse
import hashlib
import os
import sys

from send2trash import send2trash


def file_hash(path):
    digest = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def scan_folder(folder):
    hashes = {}
    for name in os.listdir(folder):
        full_path = os.path.join(folder, name)
        if not os.path.isfile(full_path):
            continue

        h = file_hash(full_path)
        hashes.setdefault(h, []).append(name)
    return [names for names in hashes.values() if len(names) > 1]


def print_report(folder, duplicates):
    total_size = 0
    total_files = 0
    to_delete = []

    for group in duplicates:
        group = sorted(group, key=lambda n: (len(n), n))
        original = group[0]
        copies = group[1:]

        print(f"Keep: {original}")

        for copy in copies:
            full = os.path.join(folder, copy)
            size = os.path.getsize(full)
            size_mb = round(size / 1024 / 1024, 2)
            print(f"  Delete: {copy} ({size_mb} MB)")
            total_size += size
            total_files += 1
            to_delete.append(full)

    print()
    print(f"Duplicate files: {total_files}")
    print(f"Wasted space: {round(total_size / 1024 / 1024, 2)} MB")
    return to_delete


def delete_files(to_delete):
    answer = input("Move these files to trash? (y/n): ").lower()
    if answer != "y":
        print("Nothing deleted")
        return

    deleted = 0
    for path in to_delete:
        if os.path.exists(path):
            send2trash(path)
            deleted += 1
    print(f"Moved to trash: {deleted}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find duplicate files by content"
    )
    parser.add_argument("folder", help="folder to scan")
    parser.add_argument(
        "--delete",
        action="store_true",
        help="offer to move the duplicates to trash",
    )
    args = parser.parse_args()

    folder = args.folder
    if not os.path.isdir(folder):
        print(f"Folder not found: {folder}")
        sys.exit(1)

    duplicates = scan_folder(folder)
    if not duplicates:
        print("No duplicates found")
        sys.exit(0)

    to_delete = print_report(folder, duplicates)

    if args.delete:
        delete_files(to_delete)
