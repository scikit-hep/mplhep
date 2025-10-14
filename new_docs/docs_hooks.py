"""MkDocs hooks for documentation generation.

This module provides hooks for MkDocs to run before building the documentation.
"""

import contextlib
import subprocess
import sys
from pathlib import Path


def on_pre_build(config):  # noqa: ARG001
    """Run before the build process starts.

    This hook runs the generate_style_guides.py script to create style-specific
    guide.md files from the template.

    Parameters
    ----------
    config : MkDocsConfig
        The MkDocs configuration object (unused)
    """
    # Get the path to the script
    docs_root = Path(__file__).parent
    script_path = docs_root / "generate_style_guides.py"

    if not script_path.exists():
        return

    # Run the generation script
    with contextlib.suppress(subprocess.CalledProcessError):
        subprocess.run(
            [sys.executable, str(script_path)],
            cwd=docs_root,
            capture_output=True,
            text=True,
            check=True,
        )
