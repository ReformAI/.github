#!/usr/bin/env python3
"""Replace a codeowner entry across all CODEOWNERS files found under a root directory."""

import argparse
import re
import sys
from pathlib import Path


def replace_codeowner(file_path: Path, old: str, new: str, dry_run: bool) -> int:
    content = file_path.read_text(encoding="utf-8")
    pattern = re.compile(r"@" + re.escape(old) + r"(?=[\s,]|$)", re.MULTILINE)

    matches = pattern.findall(content)
    if not matches:
        return 0

    new_content = pattern.sub(f"@{new}", content)

    if dry_run:
        print(f"\n[dry-run] {file_path}  ({len(matches)} occurrence(s))")
        for i, (orig, updated) in enumerate(
            zip(content.splitlines(), new_content.splitlines()), start=1
        ):
            if orig != updated:
                print(f"  line {i}:  {orig}")
                print(f"          -> {updated}")
    else:
        _ = file_path.write_text(new_content, encoding="utf-8")
        print(f"Updated {file_path}  ({len(matches)} occurrence(s))")

    return len(matches)


def find_codeowners(root: Path) -> list[Path]:
    """Return all CODEOWNERS files one level deep: <root>/*/.github/CODEOWNERS."""
    found: list[Path] = []
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        candidate = child / ".github" / "CODEOWNERS"
        if candidate.is_file():
            found.append(candidate)
    return found


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Replace a codeowner across every repo folder in a directory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
# Run from the GitHub folder — replaces @alice with @bob in all repos
python update_codeowners.py --old alice --new bob

# @ prefix is optional
python update_codeowners.py --old @alice --new @bob

# Works with org/team entries too
python update_codeowners.py --old my-org/old-team --new my-org/new-team

# Preview without writing
python update_codeowners.py --old alice --new bob --dry-run

# Target a specific root directory
python update_codeowners.py --old alice --new bob --root C:/path/to/repos
        """,
    )
    _ = parser.add_argument("--old", required=True, help="Codeowner to replace (with or without @)")
    _ = parser.add_argument("--new", required=True, help="Replacement codeowner (with or without @)")
    _ = parser.add_argument(
        "--root",
        default=".",
        help="Root directory containing repo folders (default: current directory)",
    )
    _ = parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing to disk",
    )

    class _Args(argparse.Namespace):
        old: str = ""
        new: str = ""
        root: str = "."
        dry_run: bool = False

    args = parser.parse_args(namespace=_Args())
    old = args.old.lstrip("@")
    new = args.new.lstrip("@")
    root = Path(args.root).resolve()
    dry_run = args.dry_run

    if not root.is_dir():
        print(f"Error: {root} is not a directory.", file=sys.stderr)
        sys.exit(1)

    files = find_codeowners(root)
    if not files:
        print(f"No .github/CODEOWNERS files found under {root}")
        sys.exit(0)

    print(f"Scanning {len(files)} CODEOWNERS file(s) under {root}")
    if dry_run:
        print("[dry-run mode — no files will be written]\n")

    total_files = 0
    total_replacements = 0

    for file_path in files:
        count = replace_codeowner(file_path, old, new, dry_run=dry_run)
        if count:
            total_files += 1
            total_replacements += count

    print(f"\nDone: {total_replacements} replacement(s) across {total_files} file(s).")
    if dry_run:
        print("Run without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
