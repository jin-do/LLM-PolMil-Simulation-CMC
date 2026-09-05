"""Compatibility entry point for the current coding-table reanalysis.

The historical implementation expected files outside the public package.
The current 4 x 5 primary analysis and sensitivity checks are conditional
summaries of archived coding, not validation of source passages.
"""
from reanalyze_outcomes import main

if __name__ == "__main__":
    main()
