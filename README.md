# .github

Special GitHub repository that contains generic files.

## Tools

### `update_codeowners.py`

Replaces a codeowner entry across all `CODEOWNERS` files found in a directory of repos.

**Setup:** Move `update_codeowners.py` to the root folder that contains all your organizational repositories (the parent directory of each repo). The script expects this layout:

```
repos-root/               ← run the script from here
  repo-a/
    .github/
      CODEOWNERS
  repo-b/
    .github/
      CODEOWNERS
  update_codeowners.py
```

**Usage:**

```bash
# Replace @alice with @bob across all repos
python update_codeowners.py --old alice --new bob

# Preview changes without writing (dry run)
python update_codeowners.py --old alice --new bob --dry-run

# @ prefix is optional
python update_codeowners.py --old @alice --new @bob

# Works with org/team entries too
python update_codeowners.py --old my-org/old-team --new my-org/new-team

# Target a specific root directory
python update_codeowners.py --old alice --new bob --root /path/to/repos
```

Requires Python 3.9+. No third-party dependencies.
