#!/usr/bin/env python3
"""
Convert all HEIC files in a chosen folder to JPG.

Requirements:
    pip install pillow pillow-heif --break-system-packages

Usage:
    python3 heic_to_jpg.py
"""

import glob
import os
import sys
import tkinter as tk
from tkinter import filedialog

try:
    from PIL import Image
    import pillow_heif
except ImportError:
    print("Missing dependencies. Install them with:")
    print("    pip install pillow pillow-heif --break-system-packages")
    sys.exit(1)


def choose_folder() -> str:
    """Open a native folder picker dialog and return the chosen path."""
    root = tk.Tk()
    root.withdraw()  # hide the empty root window
    folder = filedialog.askdirectory(title="Select folder containing HEIC files")
    root.destroy()
    return folder


def ask_yes_no(prompt: str) -> bool:
    while True:
        answer = input(f"{prompt} [y/n]: ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")


def convert_folder(folder: str, quality: int = 90) -> list[str]:
    """Convert HEIC files in folder to JPG. Returns list of successfully
    converted original file paths."""
    pillow_heif.register_heif_opener()

    # Match .heic / .HEIC / .Heic etc.
    patterns = [os.path.join(folder, ext) for ext in ("*.heic", "*.HEIC", "*.Heic")]
    files = sorted(set(f for pattern in patterns for f in glob.glob(pattern)))

    if not files:
        print(f"No HEIC files found in: {folder}")
        return []

    print(f"Found {len(files)} HEIC file(s) in {folder}\n")

    successful = []
    failed = 0
    for f in files:
        out_path = os.path.splitext(f)[0] + ".jpg"
        try:
            img = Image.open(f)
            img.convert("RGB").save(out_path, quality=quality)
            # Verify the JPG was actually written and is non-empty before
            # trusting it enough to delete the original later.
            if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                print(f"  ✓ {os.path.basename(f)} -> {os.path.basename(out_path)}")
                successful.append(f)
            else:
                print(f"  ✗ {os.path.basename(f)} failed: output file missing/empty")
                failed += 1
        except Exception as e:
            print(f"  ✗ {os.path.basename(f)} failed: {e}")
            failed += 1

    print(f"\nDone. {len(successful)} converted, {failed} failed.")
    return successful


def delete_originals(files: list[str]) -> None:
    deleted, errors = 0, 0
    for f in files:
        try:
            os.remove(f)
            deleted += 1
        except Exception as e:
            print(f"  ✗ Could not delete {os.path.basename(f)}: {e}")
            errors += 1
    print(f"Deleted {deleted} original file(s)." + (f" {errors} could not be deleted." if errors else ""))


def main():
    folder = choose_folder()
    if not folder:
        print("No folder selected. Exiting.")
        return

    successful = convert_folder(folder)

    if not successful:
        print("No files were successfully converted, nothing to delete.")
        return

    print()
    if ask_yes_no(f"Delete the {len(successful)} original HEIC file(s) that were successfully converted?"):
        delete_originals(successful)
    else:
        print("Originals kept.")


if __name__ == "__main__":
    main()